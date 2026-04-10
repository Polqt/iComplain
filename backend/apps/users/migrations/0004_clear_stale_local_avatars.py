"""
Data migration: clear avatar_file records that point to local filesystem paths.

When Cloudinary is active, avatar_file.url returns a Cloudinary URL like:
  https://res.cloudinary.com/.../media/avatars/...
But files uploaded before Cloudinary was configured were never sent to Cloudinary,
so those URLs return 404. This migration clears those stale references so users
see their initials instead of a broken image.
"""

from django.db import migrations


def clear_stale_local_avatars(apps, schema_editor):
    CustomUser = apps.get_model("users", "CustomUser")
    cleared = 0
    for user in CustomUser.objects.exclude(avatar_file="").exclude(avatar_file=None):
        name = user.avatar_file.name or ""
        # Cloudinary-uploaded files get a public_id that does NOT start with
        # "media/" — local files always have paths like "avatars/..." or
        # "media/avatars/...". Clear anything that looks like a local path.
        try:
            url = user.avatar_file.url
            # If the storage backend is Cloudinary, a freshly uploaded file's
            # URL starts with https://res.cloudinary.com and its name will NOT
            # contain a file extension at the path root level in the same way.
            # Safest heuristic: if the file name starts with "avatars/" it was
            # stored locally (Cloudinary renames to the public_id we pass).
            if name.startswith("avatars/") or name.startswith("media/"):
                user.avatar_file = None
                user.save(update_fields=["avatar_file"])
                cleared += 1
        except Exception:
            # Storage backend raised — file definitely not accessible, clear it
            user.avatar_file = None
            user.save(update_fields=["avatar_file"])
            cleared += 1

    if cleared:
        print(f"\n  Cleared {cleared} stale local avatar reference(s).")


def reverse_migration(apps, schema_editor):
    pass  # Irreversible — cleared file references cannot be restored


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_add_avatar_file"),
    ]

    operations = [
        migrations.RunPython(
            clear_stale_local_avatars,
            reverse_migration,
        ),
    ]

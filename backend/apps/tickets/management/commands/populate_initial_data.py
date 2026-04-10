from django.core.management.base import BaseCommand
from apps.tickets.models import Category, TicketPriority


class Command(BaseCommand):
    help = 'Populate initial data for Categories and Priorities'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating initial data...')
        
        # Create Categories
        categories = [
            'Air Conditioning & Ventilation',
            'Campus Equipment',
            'Classroom Facilities',
            'Cleanliness & Waste Management',
            'Infrastructure & Building Maintenance',
            'Internet & Connectivity',
            'Lighting & Electrical',
            'Outdoor Facilities & Grounds',
            'Restroom & Sanitation',
            'Safety & Security Concerns',
        ]

        for name in categories:
            category, created = Category.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))
        
        # Create Priorities
        priorities = [
            {'name': 'Low', 'level': 1, 'color_code': '#9ca3af'},
            {'name': 'Medium', 'level': 2, 'color_code': '#3b82f6'},
            {'name': 'High', 'level': 3, 'color_code': '#f59e0b'},
            {'name': 'Urgent', 'level': 4, 'color_code': '#ef4444'},
        ]
        
        for priority_data in priorities:
            priority, created = TicketPriority.objects.get_or_create(
                name=priority_data['name'],
                defaults={
                    'level': priority_data['level'],
                    'color_code': priority_data['color_code']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created priority: {priority.name}'))
            else:
                # Update color_code if it's still the old default
                if priority.color_code == '#6b7280':
                    priority.color_code = priority_data['color_code']
                    priority.save(update_fields=['color_code'])
                    self.stdout.write(self.style.SUCCESS(f'✓ Updated priority color: {priority.name}'))
        
        self.stdout.write(self.style.SUCCESS('\nInitial data population complete!'))
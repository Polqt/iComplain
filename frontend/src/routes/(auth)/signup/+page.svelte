<script lang="ts">
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import {
    isValidEmail,
    validatePassword,
    validatePasswordMatch,
  } from "../../../utils/validations.ts";
  import AuthLayout from "../../../components/layout/AuthLayout.svelte";

  let email: string = "";
  let password: string = "";
  let confirmPassword: string = "";
  let isLoading: boolean = false;

  let emailError: string = "";
  let passwordError: string = "";
  let confirmPasswordError: string = "";
  let generalError: string = "";
  let passwordStrength: "weak" | "medium" | "strong" = "weak";

  const strengthBarColor: Record<string, string> = {
    weak: "bg-error",
    medium: "bg-warning",
    strong: "bg-success",
  };

  const strengthColor: Record<string, string> = {
    weak: "text-error",
    medium: "text-warning",
    strong: "text-success",
  };

  function handleEmailBlur(): void {
    const result = isValidEmail(email);
    emailError = result.valid ? "" : result.message;
  }

  function handlePasswordInput(): void {
    const result = validatePassword(password);
    passwordError = result.valid ? "" : result.message;
    passwordStrength = result.strength ?? "weak";

    if (confirmPassword) {
      handleConfirmPasswordBlur();
    }
  }

  function handleConfirmPasswordBlur(): void {
    const result = validatePasswordMatch(password, confirmPassword);
    confirmPasswordError = result.valid ? "" : result.message;
  }

  async function handleSignup(event?: Event): Promise<void> {
    if (event) event.preventDefault();

    const emailValidation = isValidEmail(email);
    const passwordValidation = validatePassword(password);
    const confirmPasswordValidation = validatePasswordMatch(
      password,
      confirmPassword,
    );

    emailError = emailValidation.valid ? "" : emailValidation.message;
    passwordError = passwordValidation.valid ? "" : passwordValidation.message;
    confirmPasswordError = confirmPasswordValidation.valid
      ? ""
      : confirmPasswordValidation.message;

    if (
      !emailValidation.valid ||
      !passwordValidation.valid ||
      !confirmPasswordValidation.valid
    ) {
      return;
    }

    isLoading = true;
    generalError = "";

    try {
      // TODO: Implement actual signup logic
      goto("/signin");
    } catch (error) {
      alert("Signup failed. Please try again.");
    } finally {
      isLoading = false;
    }
  }

  function handleLoginRedirect() {
    goto("/signin");
  }
</script>

<AuthLayout>
  <div class="space-y-8">
    {#if generalError}
      <div class="alert alert-error">
        <Icon icon="mdi:alert-circle" width="20" height="20" />
        <span>{generalError}</span>
      </div>
    {/if}

    <form onsubmit={handleSignup} class="space-y-5">
      <div class="form-control">
        <label for="signup-email" class="label">
          <span class="label-text font-medium">Email Address</span>
        </label>
        <div class="relative">
          <div
            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-base-content/40"
          >
            <Icon icon="mdi:email-outline" width="20" height="20" />
          </div>
          <input
            id="signup-email"
            type="email"
            placeholder="your.id@usls.edu.ph"
            class="input input-bordered w-full pl-10 {emailError
              ? 'input-error'
              : ''}"
            class:input-success={!emailError && email}
            bind:value={email}
            onblur={handleEmailBlur}
            disabled={isLoading}
            required
          />
        </div>
        {#if emailError}
          <!-- svelte-ignore a11y_label_has_associated_control -->
          <label aria-label="email" class="label">
            <span class="label-text-alt text-error">{emailError}</span>
          </label>
        {/if}
      </div>

      <div class="form-control">
        <label for="signup-password" class="label">
          <span class="label-text font-medium">Password</span>
        </label>
        <div class="relative">
          <div
            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-base-content/40"
          >
            <Icon icon="mdi:lock-outline" width="20" height="20" />
          </div>
          <input
            id="signup-password"
            type="password"
            placeholder="Create a strong password"
            class="input input-bordered w-full pl-10 {passwordError
              ? 'input-error'
              : ''}"
            bind:value={password}
            oninput={handlePasswordInput}
            disabled={isLoading}
            required
            minlength="8"
          />
        </div>
        {#if password}
          <div class="mt-2">
            <div class="flex gap-1 mb-1">
              <div
                class="h-1 flex-1 rounded-full bg-base-300 {password.length >= 1
                  ? strengthBarColor[passwordStrength]
                  : ''}"
              ></div>
              <div
                class="h-1 flex-1 rounded-full bg-base-300 {passwordStrength !==
                'weak'
                  ? strengthBarColor[passwordStrength]
                  : ''}"
              ></div>
              <div
                class="h-1 flex-1 rounded-full bg-base-300 {passwordStrength ===
                'strong'
                  ? strengthBarColor[passwordStrength]
                  : ''}"
              ></div>
            </div>
            <!-- svelte-ignore a11y_label_has_associated_control -->
            <label class="label">
              <span class={strengthColor[passwordStrength]}>
                {passwordError || "Password strength: " + passwordStrength}
              </span>
            </label>
          </div>
        {/if}
      </div>

      <div class="form-control">
        <label for="signup-confirm-password" class="label">
          <span class="label-text font-medium">Confirm Password</span>
        </label>
        <div class="relative">
          <div
            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-base-content/40"
          >
            <Icon icon="mdi:lock-outline" width="20" height="20" />
          </div>
          <input
            id="signup-confirm-password"
            type="password"
            placeholder="Create a strong password"
            class="input input-bordered w-full pl-10 {confirmPasswordError
              ? 'input-error'
              : ''}"
            class:input-success={!confirmPasswordError && confirmPassword}
            bind:value={confirmPassword}
            onblur={handleConfirmPasswordBlur}
            disabled={isLoading}
            required
            minlength="8"
          />
        </div>
        {#if confirmPasswordError}
          <!-- svelte-ignore a11y_label_has_associated_control -->
          <label class="label">
            <span class="label-text-alt text-error">{confirmPasswordError}</span
            >
          </label>
        {:else if confirmPassword && !confirmPasswordError}
          <!-- svelte-ignore a11y_label_has_associated_control -->
          <label class="label">
            <span class="label-text-alt text-success flex items-center gap-1">
              <Icon icon="lucide:check" width="14" height="14" />
              Passwords match
            </span>
          </label>
        {/if}
      </div>

      <button
        type="submit"
        class="btn btn-primary w-full group hover:scale-105 active:scale-95 hover:shadow-xl transition-all duration-200"
        disabled={isLoading}
      >
        {#if isLoading}
          <span class="loading loading-spinner loading-sm">
            Signing Up...
          </span>
        {:else}
          <span class="flex items-center gap-2">Sign Up</span>
        {/if}
      </button>
    </form>

    <div class="text-center pt-4">
      <p class="text-sm text-base-content/60">
        Already have an account?
        <button
          type="button"
          class="link link-primary font-medium hover:link-hover"
          onclick={handleLoginRedirect}
          disabled={isLoading}
        >
          Sign In
        </button>
      </p>
    </div>
  </div>
</AuthLayout>

<script lang="ts">
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import {
    isValidEmail,
    validatePassword,
  } from "../../../utils/validations.ts";
  import {
    getRememberEmail,
    handleAuthError,
    handleRememberMe,
  } from "../../../utils/auth-helpers.ts";

  let email: string = "";
  let password: string = "";
  let rememberMe: boolean = !!getRememberEmail();
  let isLoading: boolean = false;

  let emailError: string = "";
  let passwordError: string = "";
  let generalError: string = "";

  function handleEmailBlur(): void {
    const result = isValidEmail(email);
    emailError = result.valid ? "" : result.message;
  }

  function handlePasswordBlur(): void {
    const result = validatePassword(password);
    passwordError = result.valid ? "" : result.message;
  }

  async function handleSignIn(): Promise<void> {
    const emailValidation = isValidEmail(email);
    const passwordValidation = validatePassword(password);

    if (!emailValidation.valid || !passwordValidation.valid) {
      emailError = emailValidation.valid ? "" : emailValidation.message;
      passwordError = passwordValidation.valid
        ? ""
        : passwordValidation.message;
      return;
    }

    isLoading = true;
    generalError = "";

    try {
      handleRememberMe(rememberMe, email);
      
      await new Promise((resolve) => setTimeout(resolve, 1000));
      goto("/dashboard");
    } catch (error) {
      generalError = handleAuthError(error);
    } finally {
      isLoading = false;
    }
  }

  async function handleGoogleSignIn() {
    isLoading = true;
    try {
      // TODO: Implement Google OAuth
      console.log("Google sign in attempt");
      // For now, just redirect to student dashboard
      await new Promise((resolve) => setTimeout(resolve, 1000));
      goto("/student/dashboard");
    } catch (error) {
      console.error("Google sign in error:", error);
      alert("Google sign in failed. Please try again.");
    } finally {
      isLoading = false;
    }
  }

  function handleSignupRedirect() {
    goto("/signup");
  }
</script>

<div class="space-y-8">
  {#if generalError}
    <div class="alert alert-error">
      <Icon icon="mdi:alert-circle" width="20" height="20" />
      <span>{generalError}</span>
    </div>
  {/if}

  <form onsubmit={handleSignIn} class="space-y-5">
    <div class="form-control">
      <label for="signin-email" class="label">Email Address</label>
      <div class="relative">
        <div
          class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-base-content/40"
        >
          <Icon icon="mdi:email-outline" width="20" height="20" />
        </div>
        <input
          id="signin-email"
          type="email"
          placeholder="your.id@usls.edu.ph"
          class="input input-bordered w-full pl-10 {emailError
            ? 'input-error'
            : ''}"
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
      <label for="signin-password" class="label">Password</label>
      <div class="relative">
        <div
          class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-base-content/40"
        >
          <Icon icon="mdi:lock-outline" width="20" height="20" />
        </div>
        <input
          id="signin-password"
          type="password"
          placeholder="Enter your password"
          class="input input-bordered w-full pl-10 {passwordError
            ? 'input-error'
            : ''}"
          class:input-success={!passwordError && password}
          bind:value={password}
          onblur={handlePasswordBlur}
          disabled={isLoading}
          required
        />
      </div>
      {#if passwordError}
        <!-- svelte-ignore a11y_label_has_associated_control -->
        <label aria-label="password" class="label">
          <span class="label-text-alt text-error">{passwordError}</span>
        </label>
      {/if}
    </div>

    <div class="flex items-center justify-between">
      <label class="label cursor-pointer gap-2 p-0">
        <input
          type="checkbox"
          class="checkbox checkbox-sm checkbox-primary"
          bind:checked={rememberMe}
          disabled={isLoading}
        />
        <span class="label-text">Remember me</span>
      </label>
    </div>

    <button
      type="submit"
      class="btn btn-primary w-full group hover:scale-105 active:scale-95 hover:shadow-xl transition-all duration-200"
      disabled={isLoading}
    >
      {#if isLoading}
        <span class="loading loading-spinner loading-sm"> Signing In... </span>
      {:else}
        <span class="flex items-center gap-2">Sign In</span>
      {/if}
    </button>
  </form>

  <div class="text-center pt-4">
    <p class="text-sm text-base-content/60">
      Don't have an account?
      <button
        type="button"
        class="link link-primary font-medium hover:link-hover"
        onclick={handleSignupRedirect}
        disabled={isLoading}
      >
        Sign up
      </button>
    </p>
  </div>
</div>

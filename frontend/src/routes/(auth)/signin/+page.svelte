<script lang="ts">
  import { onMount, tick } from "svelte";
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import { authStore } from "../../../stores/auth.store.ts";
  import { GOOGLE_CLIENT_ID } from "../../../utils/api.ts";
  import {
    isValidEmail,
    validatePassword,
  } from "../../../utils/validations.ts";
  import {
    getRememberEmail,
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
      await authStore.loginWithEmailPassword(email, password);
      handleRememberMe(rememberMe, email);
      goto("/dashboard");
    } catch (error) {
      generalError =
        error instanceof Error
          ? error.message
          : "Sign-in failed. Please try again.";
    } finally {
      isLoading = false;
    }
  }

  function getErrorMessage(err: unknown): string {
    if (err instanceof Error) return err.message;
    if (
      typeof err === "object" &&
      err !== null &&
      "message" in err &&
      typeof (err as { message: unknown }).message === "string"
    ) {
      return (err as { message: string }).message;
    }
    return "Google sign-in failed. Please try again.";
  }

  async function handleGoogleCallback(response: {
    credential: string;
  }): Promise<void> {
    generalError = "";
    isLoading = true;
    try {
      await authStore.loginWithGoogle(response.credential);
      goto("/dashboard");
    } catch (err) {
      generalError = getErrorMessage(err);
    } finally {
      isLoading = false;
      (document.activeElement as HTMLElement)?.blur();
    }
  }

  function handleGoogleSignIn(): void {
    const g = (
      window as unknown as {
        google?: {
          accounts: {
            id: {
              prompt: () => void;
            };
          };
        };
      }
    ).google;

    if (g?.accounts?.id) {
      g.accounts.id.prompt();
    }
  }

  onMount(async () => {
    await tick();
    if (!GOOGLE_CLIENT_ID) return;

    let retryCount = 0;
    const MAX_RETRIES = 50;

    const initGoogle = () => {
      const g = (
        window as unknown as {
          google?: {
            accounts: {
              id: {
                initialize: (c: object) => void;
              };
            };
          };
        }
      ).google;

      if (!g?.accounts?.id) {
        retryCount += 1;
        if (retryCount > MAX_RETRIES) {
          generalError =
            "Google sign-in is unavailable. Please check your connection or disable any script blockers and try again.";
          return;
        }
        setTimeout(initGoogle, 100);
        return;
      }

      g.accounts.id.initialize({
        client_id: GOOGLE_CLIENT_ID,
        callback: (res: { credential: string }) => handleGoogleCallback(res),
      });
    };

    initGoogle();
  });
</script>

<div class="w-full">
  <!-- Header -->
  <div class="mb-10">
    <h2 class="text-3xl lg:text-4xl font-bold text-base-content mb-3">
      Sign In
    </h2>
    <p class="text-base text-base-content/60">
      Enter your credentials to access your account
    </p>
  </div>

  <!-- Error Alert -->
  {#if generalError}
    <div
      class="alert bg-error/10 border border-error/20 text-error mb-6 rounded-xl py-3"
    >
      <Icon icon="mdi:alert-circle" width="20" height="20" />
      <span class="text-sm">{generalError}</span>
    </div>
  {/if}

  <!-- Sign In Form -->
  <form
    onsubmit={(event) => {
      event.preventDefault();
      void handleSignIn();
    }}
    class="space-y-5"
  >
    <!-- Email Field -->
    <div class="form-control">
      <label for="signin-email" class="label pb-2">
        <span class="label-text font-semibold text-base-content text-sm"
          >Email Address</span
        >
      </label>
      <div class="relative">
        <div
          class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-base-content/40"
        >
          <Icon icon="mdi:email-outline" width="20" height="20" />
        </div>
        <input
          id="signin-email"
          type="email"
          placeholder="your.id@usls.edu.ph"
          class="input input-bordered w-full pl-11 h-12 rounded-xl bg-base-100 border-base-300 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500/20 transition-all placeholder:text-base-content/40 {emailError
            ? 'border-error focus:border-error focus:ring-error/20'
            : ''}"
          bind:value={email}
          onblur={handleEmailBlur}
          disabled={isLoading}
          required
        />
      </div>
      {#if emailError}
        <!-- svelte-ignore a11y_label_has_associated_control -->
        <label aria-label="email" class="label pt-2">
          <span
            class="label-text-alt text-error flex items-center gap-1 text-xs"
          >
            <Icon icon="mdi:alert-circle-outline" width="14" height="14" />
            {emailError}
          </span>
        </label>
      {/if}
    </div>

    <!-- Password Field -->
    <div class="form-control">
      <label for="signin-password" class="label pb-2">
        <span class="label-text font-semibold text-base-content text-sm"
          >Password</span
        >
      </label>
      <div class="relative">
        <div
          class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-base-content/40"
        >
          <Icon icon="mdi:lock-outline" width="20" height="20" />
        </div>
        <input
          id="signin-password"
          type="password"
          placeholder="Enter your password"
          class="input input-bordered w-full pl-11 h-12 rounded-xl bg-base-100 border-base-300 focus:border-green-500 focus:outline-none focus:ring-2 focus:ring-green-500/20 transition-all placeholder:text-base-content/40 {passwordError
            ? 'border-error focus:border-error focus:ring-error/20'
            : ''}"
          bind:value={password}
          onblur={handlePasswordBlur}
          disabled={isLoading}
          required
        />
      </div>
      {#if passwordError}
        <!-- svelte-ignore a11y_label_has_associated_control -->
        <label aria-label="password" class="label pt-2">
          <span
            class="label-text-alt text-error flex items-center gap-1 text-xs"
          >
            <Icon icon="mdi:alert-circle-outline" width="14" height="14" />
            {passwordError}
          </span>
        </label>
      {/if}
    </div>

    <!-- Remember Me -->
    <div class="flex items-center pt-1">
      <label class="label cursor-pointer gap-3 p-0">
        <input
          type="checkbox"
          class="checkbox checkbox-sm checkbox-success border-2 border-base-300"
          bind:checked={rememberMe}
          disabled={isLoading}
        />
        <span class="label-text text-base-content/70 text-sm">Remember me</span>
      </label>
    </div>

    <!-- Submit Button -->
    <button
      type="submit"
      class="btn w-full h-12 rounded-xl text-white font-semibold border-0 bg-green-600 hover:bg-green-700 transition-all duration-200 hover:shadow-lg hover:shadow-green-600/25 disabled:bg-green-600/50 normal-case text-base mt-6"
      disabled={isLoading}
    >
      {#if isLoading}
        <span class="loading loading-spinner loading-sm"></span>
        <span>Signing in...</span>
      {:else}
        <span>Sign In</span>
        <Icon icon="mdi:arrow-right" width="20" height="20" />
      {/if}
    </button>
  </form>

  <!-- Google Sign In -->
  {#if GOOGLE_CLIENT_ID}
    <div class="mt-6 space-y-4">
      <div class="relative flex items-center justify-center">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-base-300"></div>
        </div>
        <div class="relative px-4 bg-base-100">
          <span
            class="text-xs font-medium text-base-content/50 uppercase tracking-wider"
            >Or continue with</span
          >
        </div>
      </div>
      <button
        type="button"
        onclick={handleGoogleSignIn}
        class="btn w-full h-12 rounded-xl font-semibold border border-base-300 bg-base-100 hover:bg-base-200/50 hover:border-base-400 transition-all duration-200 normal-case text-base flex items-center justify-center gap-3"
        disabled={isLoading}
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 20 20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M19.6 10.227c0-.709-.064-1.39-.182-2.045H10v3.868h5.382a4.6 4.6 0 01-1.996 3.018v2.51h3.232c1.891-1.742 2.982-4.305 2.982-7.35z"
            fill="#4285F4"
          />
          <path
            d="M10 20c2.7 0 4.964-.895 6.618-2.423l-3.232-2.509c-.895.6-2.04.955-3.386.955-2.605 0-4.81-1.76-5.595-4.123H1.064v2.59A9.996 9.996 0 0010 20z"
            fill="#34A853"
          />
          <path
            d="M4.405 11.9c-.2-.6-.314-1.24-.314-1.9 0-.66.114-1.3.314-1.9V5.51H1.064A9.996 9.996 0 000 10c0 1.614.386 3.14 1.064 4.49l3.34-2.59z"
            fill="#FBBC05"
          />
          <path
            d="M10 3.977c1.468 0 2.786.505 3.823 1.496l2.868-2.868C14.959.99 12.695 0 10 0 6.09 0 2.71 2.24 1.064 5.51l3.34 2.59C5.19 5.736 7.395 3.977 10 3.977z"
            fill="#EA4335"
          />
        </svg>
        <span>Continue with Google</span>
      </button>
    </div>
  {/if}
</div>

<style>
  :global([data-sveltekit-preload-data]) {
    cursor: default;
  }
</style>

<script lang="ts">
  import { onMount, tick } from "svelte";
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import { authStore } from "../../../stores/auth.store.ts";
  import { API_BASE, GOOGLE_CLIENT_ID } from "../../../utils/api.ts";
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
  let googleButtonEl: HTMLDivElement;
  let googleWrapperEl: HTMLDivElement;

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
        error instanceof Error ? error.message : "Sign-in failed. Please try again.";
    } finally {
      isLoading = false;
    }
  }

  function getErrorMessage(err: unknown): string {
    if (err instanceof Error) return err.message;
    if (typeof err === "object" && err !== null && "message" in err && typeof (err as { message: unknown }).message === "string") {
      return (err as { message: string }).message;
    }
    return "Google sign-in failed. Please try again.";
  }

  async function handleGoogleCallback(response: { credential: string }): Promise<void> {
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

  function handleSignupRedirect() {
    goto("/signup");
  }

  onMount(async () => {
    await tick();
    if (!GOOGLE_CLIENT_ID || !googleButtonEl || !googleWrapperEl) return;

    let retryCount = 0;
    const MAX_RETRIES = 50; 

    const initGoogle = () => {
      const g = (window as unknown as {
        google?: {
          accounts: {
            id: {
              initialize: (c: object) => void;
              renderButton: (el: HTMLElement, o: object) => void;
            };
          };
        };
      }).google;

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
      const width = Math.max(googleWrapperEl.offsetWidth || 320, 320);
      g.accounts.id.renderButton(googleButtonEl, {
        type: "standard",
        theme: "outline",
        size: "large",
        width,
        text: "continue_with",
      });
    };

    initGoogle();
  });
</script>

<div class="space-y-8 max-w-100">
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

  {#if GOOGLE_CLIENT_ID}
    <div class="flex items-center gap-4 my-6">
      <div class="flex-1 h-px bg-base-content/20"></div>
      <span class="text-sm text-base-content/60">or</span>
      <div class="flex-1 h-px bg-base-content/20"></div>
    </div>
    <div
      class="flex w-full transition-transform duration-200 hover:scale-[1.02] active:scale-[0.98]"
      bind:this={googleWrapperEl}
    >
      <div
        class="w-full min-h-12 rounded-btn overflow-hidden"
        bind:this={googleButtonEl}
      ></div>
    </div>
  {/if}
</div>

<script>
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import Footer from "../../../components/layout/Footer.svelte";
  import Header from "../../../components/layout/Header.svelte";

  let email = "";
  let password = "";
  let isLoading = false;

  async function handleLogin() {
    isLoading = true;
    try {
      // TODO: Implement actual login logic
      console.log("Login attempt:", { email, password });
      // For now, just redirect to student dashboard
      await new Promise(resolve => setTimeout(resolve, 1000)); 
      goto("/student/dashboard");
    } catch (error) {
      console.error("Login error:", error);
      alert("Login failed. Please check your credentials and try again.");
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
      await new Promise(resolve => setTimeout(resolve, 1000));
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

<div class="w-full flex flex-col items-center bg-base-100 min-h-screen">
  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8">
    <Header />
  </div>

  <main class="w-full max-w-4xl px-4 sm:px-6 lg:px-8 flex-1 flex items-center justify-center py-12 sm:py-16">
    <div class="w-full max-w-md">
      <div class="card bg-base-100 shadow-xl border border-base-300">
        <div class="card-body p-6 sm:p-8">
          <div class="text-center mb-6">
            <p class="badge badge-ghost text-xs font-semibold tracking-widest uppercase mb-4">
              Welcome Back
            </p>
            <h1 class="text-2xl sm:text-3xl font-semibold text-base-content leading-tight">
              Sign In to iComplain
            </h1>
            <p class="text-sm sm:text-base text-base-content/60 mt-2">
              Access your account to report and track issues
            </p>
          </div>

          <form on:submit|preventDefault={handleLogin} class="space-y-4">
            <div class="form-control w-full">
              <label class="label" for="login-email">
                <span class="label-text text-base font-medium">Email</span>
              </label>
              <input
                id="login-email"
                type="email"
                placeholder="your.email@usls.edu.ph"
                class="input input-bordered w-full"
                bind:value={email}
                required
                disabled={isLoading}
              />
            </div>

            <div class="form-control w-full">
              <label class="label" for="login-password">
                <span class="label-text text-base font-medium">Password</span>
              </label>
              <input
                id="login-password"
                type="password"
                placeholder="Enter your password"
                class="input input-bordered w-full"
                bind:value={password}
                required
                disabled={isLoading}
              />
            </div>

            <div class="form-control mt-6">
              <button
                class="btn btn-primary btn-block group hover:scale-105 active:scale-95 hover:shadow-xl transition-all duration-200"
                type="submit"
                disabled={isLoading}
              >
                {#if isLoading}
                  <span class="loading loading-spinner loading-sm"></span>
                  Signing In...
                {:else}
                  <span class="flex items-center justify-center gap-2">
                    Sign In
                    <Icon
                      icon="lucide:log-in"
                      width="20"
                      height="20"
                      class="transition-transform group-hover:translate-x-1 duration-300"
                    />
                  </span>
                {/if}
              </button>
            </div>
          </form>

          <div class="divider my-6">or</div>

          <div class="space-y-3">
            <button
              class="btn btn-outline btn-block group hover:scale-105 active:scale-95 hover:shadow-lg transition-all duration-200"
              type="button"
              on:click={handleGoogleSignIn}
              disabled={isLoading}
            >
              <span class="flex items-center justify-center gap-2">
                <Icon
                  icon="logos:google-icon"
                  width="20"
                  height="20"
                  class="transition-transform group-hover:scale-110 duration-300"
                />
                Sign in with Google
              </span>
            </button>
          </div>

          <div class="text-center mt-6">
            <p class="text-sm text-base-content/60">
              Don't have an account?
              <button
                type="button"
                class="link link-primary font-medium"
                on:click={handleSignupRedirect}
                disabled={isLoading}
              >
                Sign up
              </button>
            </p>
          </div>

          <div class="text-center mt-4">
            <p class="text-xs text-base-content/45">
              By signing in, you agree to our Terms of Service and Privacy Policy.
            </p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <div class="w-full max-w-7xl px-4 sm:px-6 lg:px-8 mt-auto">
    <div class="border-t border-base-content/10"></div>
    <Footer />
  </div>
</div>
<script>
  import { goto } from "$app/navigation";
  import Icon from "@iconify/svelte";
  import Footer from "../../components/layout/Footer.svelte";
  import Header from "../../components/layout/Header.svelte";

  let email = "";
  let password = "";
  let confirmPassword = "";
  let isLoading = false;

  async function handleSignup() {
    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    isLoading = true;
    try {
      // TODO: Implement actual signup logic
      console.log("Signup attempt:", { email, password });
      // For now, just redirect to login
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      goto("/login");
    } catch (error) {
      console.error("Signup error:", error);
      alert("Signup failed. Please try again.");
    } finally {
      isLoading = false;
    }
  }

  function handleLoginRedirect() {
    goto("/login");
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
              Create Account
            </p>
            <h1 class="text-2xl sm:text-3xl font-semibold text-base-content leading-tight">
              Join iComplain
            </h1>
            <p class="text-sm sm:text-base text-base-content/60 mt-2">
              Sign up to start reporting and resolving issues.
            </p>
          </div>

          <form on:submit|preventDefault={handleSignup} class="space-y-4">
            <div class="form-control w-full">
              <label class="label" for="email">
                <span class="label-text text-base font-medium">Email</span>
              </label>
              <input
                id="email"
                type="email"
                placeholder="your.email@usls.edu.ph"
                class="input input-bordered w-full"
                bind:value={email}
                required
                disabled={isLoading}
              />
            </div>

            <div class="form-control w-full">
              <label class="label" for="password">
                <span class="label-text text-base font-medium">Password</span>
              </label>
              <input
                id="password"
                type="password"
                placeholder="Create a strong password"
                class="input input-bordered w-full"
                bind:value={password}
                required
                minlength="8"
                disabled={isLoading}
              />
            </div>

            <div class="form-control w-full">
              <label class="label" for="confirmPassword">
                <span class="label-text text-base font-medium">Confirm Password</span>
              </label>
              <input
                id="confirmPassword"
                type="password"
                placeholder="Confirm your password"
                class="input input-bordered w-full"
                bind:value={confirmPassword}
                required
                minlength="8"
                disabled={isLoading}
              />
            </div>

            <button
              class="btn btn-primary btn-block mt-6 group hover:scale-105 active:scale-95 hover:shadow-xl transition-all duration-200"
              type="submit"
              disabled={isLoading}
            >
              {#if isLoading}
                <span class="loading loading-spinner loading-sm"></span>
                Creating Account...
              {:else}
                <span class="flex items-center justify-center gap-2">
                  Create Account
                  <Icon
                    icon="lucide:user-plus"
                    width="20"
                    height="20"
                    class="transition-transform group-hover:translate-x-1 duration-300"
                  />
                </span>
              {/if}
            </button>
          </form>

          <div class="divider my-6">or</div>

          <div class="text-center">
            <p class="text-sm text-base-content/60">
              Already have an account?
              <button
                type="button"
                class="link link-primary font-medium"
                on:click={handleLoginRedirect}
                disabled={isLoading}
              >
                Sign in
              </button>
            </p>
          </div>

          <div class="text-center mt-6">
            <p class="text-xs text-base-content/45">
              By creating an account, you agree to our Terms of Service and Privacy Policy.
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
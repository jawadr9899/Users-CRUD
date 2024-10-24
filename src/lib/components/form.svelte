<script lang="ts">
  export let url: string;
  export let method: string;
  export let title: string;

  let name: string, email: string, password: string;
  let loading = false,
    isSent = false;

  console.log(url, method, title);
  async function handleForm(e: SubmitEvent): Promise<boolean> {
    e.preventDefault();
    // validate
    if (name.length < 3 && email.length < 5 && password.length < 5) {
      return false;
    }
    // send to backend
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 5000);
      const data = {
        name,
        email,
        password,
      };
      loading = true;
      const res = await fetch(url, {
        method,
        headers: {
          "Content-type": "application/json",
          Connection: "keep-alive",
        },
        body: JSON.stringify(data),
        signal: controller.signal,
      });
      // clear the form & timeout
      name = email = password = "";
      clearTimeout(timeout);
      // get response
      const jsonData = await res.json();
      if (!jsonData?.success) {
        controller.abort();
      }
      loading = false;
      isSent = true;

      setTimeout(() => {
        isSent = false;
      }, 5000);
    } catch (e) {
      console.log("Error handleForm():\n", e);
      loading = false;
      return false;
    }

    return true;
  }
</script>

<form
  class="lg:w-1/3 md:w-1/2 bg-white flex flex-col md:mx-auto text-center w-full md:py-8 mt-8 md:mt-0"
  on:submit={handleForm}
>
  <h1 class="text-gray-900 text-3xl mb-1 font-medium title-font uppercase">
    {title} A NEW USER
  </h1>
  <p class="leading-relaxed mb-5 text-gray-600">
    [CRUD] Operations Can Be Performed On Added Users
  </p>
  <div class="relative mb-4">
    <input
      type="text"
      id="name"
      bind:value={name}
      name="name"
      placeholder="Name"
      class="w-full bg-white rounded border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
    />
  </div>
  <div class="relative mb-4">
    <input
      type="email"
      id="email"
      placeholder="Email"
      name="email"
      bind:value={email}
      class="w-full bg-white rounded border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
    />
  </div>
  <div class="relative mb-4">
    <input
      type="password"
      bind:value={password}
      id="password"
      placeholder="Password"
      name="password"
      class="w-full bg-white rounded border border-gray-300 focus:border-red-500 focus:ring-2 focus:ring-red-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
    />
  </div>
  <button
    class={`text-white bg-red-500 border-0 py-2 px-6 focus:outline-none ${loading && "bg-gray-400"}hover:bg-red-600 rounded text-lg`}
  >
    {loading ? "Loading..." : title}</button
  >
  <br />
  {#if isSent}
    <a href="/view">View</a>
  {/if}
</form>

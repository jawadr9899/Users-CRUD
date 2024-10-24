<script lang="ts">
  import { onMount } from "svelte";

  type User = { id: string; name: string; email: string; password: string };

  let data: User[];
  const url = "http://127.0.0.1:3000/users";

  onMount(async () => {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      data = await response.json();
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  });

  async function deleteUser(id: string) {
    data = data.filter((u) => u.id !== id);
    try {
      const res = await fetch(`${url}/${id}`, {
        method: "DELETE",
        headers: {
          Connection: "keep-alive",
        },
      });
      const data = await res.json();
      if (!data?.success) {
        console.error("Error cannot delete user! deleteUser()");
      }
      console.log(data);
    } catch (error) {
      console.log("Error at deleteUser():\n", error);
    }
  }
</script>

<section class="text-gray-600 body-font">
  <div class="container px-5 py-24 mx-auto">
    <div class="flex flex-wrap -m-4">
      {#if data}
        {#each data as item}
          <div class="xl:w-1/4 md:w-1/2 p-4">
            <div class="bg-gray-100 p-6 rounded-lg">
              <img
                class="h-40 rounded w-full object-cover object-center mb-6"
                src="https://dummyimage.com/720x400"
                alt="content"
              />
              <h3
                class="tracking-widest text-indigo-500 text-xs font-medium title-font"
              >
                {item.name}
              </h3>
              <h2 class="text-lg text-gray-900 font-medium title-font mb-4">
                {item.email}
              </h2>
              <p class="leading-relaxed text-base">
                {item.password.substring(0, 10)}
              </p>
              <div>
                <button
                  type="button"
                  class=" text-white px-3 py-1 mt-2 rounded-lg bg-red-500 mr-3"
                  on:click={() => deleteUser(item.id)}>DELETE</button
                >
                <a
                  href={`/update/${item.id}`}
                  class=" text-white px-3 py-1 mt-2 rounded-lg bg-green-500"
                  >UPDATE</a
                >
              </div>
            </div>
          </div>
        {/each}
      {:else}
        <h1 class="text-4xl text-white">Fetching...</h1>
      {/if}

      {#if data && data.length === 0}
        <h1 class="text-center mx-auto">
          <p>No Users Found!</p>
          <br />
          <a href="/" class=" text-white px-3 py-1 mt-2 rounded-lg bg-blue-500"
            >Add New Users</a
          >
        </h1>
      {/if}
    </div>
  </div>
</section>

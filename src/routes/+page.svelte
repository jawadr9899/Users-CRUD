<script lang="ts">
  import Form from "$lib/components/form.svelte";
</script>

<div class="text-center mb-1">
  <h1 class="text-red-400">Hello From</h1>
  <h1 class="text-4xl text-red-600">SvelteKit</h1>
</div>

<Form title={"Add"} method={"POST"} url={`http://127.0.0.1:3000/users`} />

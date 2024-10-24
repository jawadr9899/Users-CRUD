<script>
  import Form from "$lib/components/form.svelte";
  import { page } from "$app/stores";
</script>

<Form
  title={"Update"}
  method={"PUT"}
  url={`http://127.0.0.1:3000/users/${$page.params.slug}`}
/>

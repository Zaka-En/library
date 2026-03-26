<script lang="ts">
  import { styleQuiz } from "$lib/questions/questions";
  import { Form } from "@library/comp-library";
</script>

<!-- center the artilce using margin -->
<article class="mx-auto my-auto">
  <Form questions={styleQuiz} />
</article>

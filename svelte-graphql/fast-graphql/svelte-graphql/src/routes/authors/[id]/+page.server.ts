import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params }) => {
  const { id } = params;

  // usar `id` para consultar la BD / GraphQL
  return { id };
}
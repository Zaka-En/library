import type { PageServerLoad } from "./$types";
import { graphql } from "$houdini"
import { redirect } from "@sveltejs/kit";

const userInfoStore = graphql(`
    query UserInfo($userId: Int!) {
      userInfo(userId: $userId) {
        city
        email
        fullname
        id
        name
        province
        rol
        secondName
        streetAdress
        zipCode
      }
    }
  `)

export const load: PageServerLoad = async (event) => {  

  const { data } = await userInfoStore.fetch({
    event,
    variables:{
      userId: event.locals.user?.id
    }
  })


  if (!data?.userInfo) {
    redirect(302, '/login')
  }

  return {
    profile: data.userInfo
  }

}
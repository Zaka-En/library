import type { PageServerLoad, Actions } from "./$types"
import { graphql } from "$houdini"
import { fail } from "@sveltejs/kit"



const userInfoStore = graphql(`
    query UserInfo($userId: Int!) {
      userInfo(userId: $userId) {
        id
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
        about
      }
    }
  `)

const updateUserInfoStore = graphql(`
    mutation UpdateUser($input: UpdateUserInput!){
      updateUser(input: $input){
        id
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
        about
      }
    }
`)

export const load: PageServerLoad = async (event) => {  

  const { data } = await userInfoStore.fetch({
    event,
    variables:{
      userId: 5 //event.locals.user?.id 
    }
  })

  // if (!data?.userInfo) {
  //   redirect(302, '/login')
  // }

  return {
    profile: data?.userInfo,
    updateProfileStore: updateUserInfoStore
  }

}

export const actions: Actions = {
  update: async (event) => {
    const formData = await event.request.formData()

    



  }
}

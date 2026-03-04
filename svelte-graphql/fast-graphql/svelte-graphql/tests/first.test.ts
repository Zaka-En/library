import { graphql, HttpResponse } from 'msw'
import {  it, expect, beforeAll, afterAll, afterEach, vi } from 'vitest'
import { setupServer } from 'msw/node'

const api = graphql.link('http://localhost:8000/grapqhql')

type Author = {
  id: string
  name: string
  fullname?: string
  biograby?: string
  country: string
}

interface GetAuthorResponse {
  author: Author | null
}

export const handlers = [
  api.query<GetAuthorResponse, {id: string}>("GetAuthor", ({ variables }) => {
    return HttpResponse.json({
      data: {
        author:  {
          id: variables.id,
          name: "George",
          fullname: "Georege RR Martin",
          country: "España"
        }
      }
    })
  })
]

const server = setupServer(...handlers)

beforeAll(() => server.listen())
afterEach(() => server.restoreHandlers())
afterAll(() => server.close())



it('should return the specific author when querying by id', async () => {
  const targetId = '123'
  
  const response = await fetch('http://localhost:8000/grapqhql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: `
        query GetAuthor($id: String!) {
          author(id: $id) {
            id
            name
            fullname
            country
          }
        }
      `,
      variables: { id: targetId },
    }),
  })

  const result = await response.json()

  expect(response.status).toBe(200)
  expect(result.data.author).toEqual({
    id: targetId,
    name: "George",
    fullname: "Georege RR Martin",
    country: "España"
  })
})


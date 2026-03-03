import { setupWorker } from 'msw/browser'
import { handlers } from './first.test'

export const worker = setupWorker(...handlers)


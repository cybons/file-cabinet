import { assertExists } from './assertions'
import { asUserId } from './userId'

const userId = asUserId('aaaa')
const root = document.querySelector<HTMLElement>('root')
assertExists(root)
console.log(userId)

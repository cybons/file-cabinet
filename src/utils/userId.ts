import { Brand, FilledString } from '../types/types'
import { assertFilledString } from './assertions'
import { PreconditionError } from './error'

export type UserId = Brand<FilledString, 'UserId'>

function assertUserId(v: FilledString, target = ''): asserts v is UserId {
  if (!(v.length > 2)) {
    throw new PreconditionError(`${target} should be not empty string`.trim())
  }
}

export function asUserId(v: unknown): UserId {
  assertFilledString(v, 'UserId')
  assertUserId(v, 'UserId')
  return v
}

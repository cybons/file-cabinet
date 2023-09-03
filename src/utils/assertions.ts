import { FilledString } from '../types/types'
import { PreconditionError } from './error'
import { isString } from './stringUtils'

export function exists<T>(v: T | null | undefined): v is NonNullable<T> {
  return typeof v !== 'undefined' && v !== null
}

export function assertExists<T>(v: T | null | undefined, target = ''): asserts v is NonNullable<T> {
  if (!exists(v)) {
    throw new Error(`${target} should be specified`.trim())
  }
}

export function isFilledString(v: unknown): v is string {
  return isString(v) && v !== ''
}

export function assertFilledString(v: unknown, target = ''): asserts v is FilledString {
  if (!isFilledString(v)) {
    throw new PreconditionError(`${target} should be not empty string`.trim())
  }
}
export function asFilledString(v: unknown, target = ''): FilledString {
  assertFilledString(v, target)
  return v
}

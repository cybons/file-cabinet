import { FileOrFolder } from '../components/fileOrFolderItem'

type Underscore<P extends string> = `__${P}`
type Underscored<T extends string> = {
  [P in T as Underscore<P>]: Underscore<P>
}
export type Brand<K, T extends string> = K & Underscored<T>
export type FilledString = Brand<string, 'FilledString'>
export type SetFileOrFolderState = React.Dispatch<React.SetStateAction<FileOrFolder[]>>

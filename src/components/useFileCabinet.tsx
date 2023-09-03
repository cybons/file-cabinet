import { useState } from 'react'
import { SetFileOrFolderState } from '../types/types'
import { FileOrFolder } from './fileOrFolderItem'

interface Result {
  items: FileOrFolder[]
  setItems: SetFileOrFolderState
  currentFolderId: string
  handler: {
    setCurrentFolderId: React.Dispatch<React.SetStateAction<string>>
    handleUploadSuccess: (fileId: string, newVersion: string) => void
    handleDeleteSuccess: (fileId: string) => void
    handleChangeNameSuccess: (fileId: string, name: string) => void
  }
}
export function uploadSuccess(setItems: SetFileOrFolderState) {
  return (fileId: string, newVersion: string): void => {
    setItems((prevItems) =>
      prevItems.map((item) => {
        if (item.id === fileId) {
          return {
            ...item,
            version: newVersion,
          }
        }
        return item
      }),
    )
  }
}
export type HandleToggleLoadingResult = {
  isLoading: boolean
  onClick: () => Promise<void>
}

function createUploadSuccessHandler(setItems: SetFileOrFolderState) {
  return (fileId: string, newVersion: string): void => {
    setItems((prevItems) =>
      prevItems.map((item) => {
        if (item.id === fileId) {
          return {
            ...item,
            version: newVersion,
          }
        }
        return item
      }),
    )
  }
}

export function useFileCabinet(initialFolderId: string): Result {
  const [items, setItems] = useState<FileOrFolder[]>([])
  const [currentFolderId, setCurrentFolderId] = useState<string>(initialFolderId)

  const handleDeleteSuccess = (fileId: string): void => {
    setItems((prevItems) => prevItems.filter((item) => item.id !== fileId))
  }

  const handleUploadSuccess = createUploadSuccessHandler(setItems)

  const handleChangeNameSuccess = (fileId: string, newName: string): void => {
    setItems((prevItems) =>
      prevItems.map((item) => {
        if (item.id === fileId) {
          return {
            ...item,
            name: newName,
          }
        }
        return item
      }),
    )
  }
  const handler = {
    setCurrentFolderId,
    handleUploadSuccess,
    handleDeleteSuccess,
    handleChangeNameSuccess,
  } as const
  return {
    items,
    setItems,
    currentFolderId,
    handler,
  }
}

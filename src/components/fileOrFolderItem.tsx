import { css } from '@acab/ecsstatic/scss'
import { SyntheticEvent, useState } from 'react'
import PromptModal from './PromptModal'
import UploadButton from './UploadButton'

// types.ts
export interface FileOrFolder {
  id: string
  name: string
  type: 'file' | 'folder'
  lastUpdated: string
  size: number
  version: string
  updatedBy: string
}
const FileItemsVersion = css`
  // ...
  color: #1004ff;
  font-weight: bold;
  &:hover,
  &:focus {
    color: red;
  }
`

interface Props {
  // setItems: SetFileOrFolderState
  item: FileOrFolder
  // onFolderDoubleClick: (folderId: string) => void
  // onUploadSuccess: (fileId: string, newVersion: string) => void
  // onUploadClick: () => void
  // onDeleteSuccess: (fileId: string) => void
  // onChangeNameSuccess: (name: string, newName: string) => void
  handler: {
    setCurrentFolderId: React.Dispatch<React.SetStateAction<string>>
    handleUploadSuccess: (fileId: string, newVersion: string) => void
    // useToggleLoading: (id: string, name: string) => HandleToggleLoadingResult
    handleDeleteSuccess: (fileId: string) => void
    handleChangeNameSuccess: (fileId: string, name: string) => void
  }
}

export function FileOrFolderItem({
  // setItems,
  item,
  handler, // onFolderDoubleClick,
  // onUploadClick,
} // onDeleteSuccess,
// onChangeNameSuccess,
: Props): JSX.Element {
  const [isPromptOpen, setPromptOpen] = useState(false)
  // const [item, setItem] = useState({ id: 1, name: 'example.txt' });

  // const onUploadClick = async (): Promise<void> => {
  //   await sleep(1)
  //   // アップロードのロジック...
  //   // 成功した場合

  //   onUploadSuccess(item.id, item.version + 4)
  // }
  // 例: 削除ボタンのonClickイベント
  const onDeleteClick = (): void => {
    // 削除のロジック...
    // 成功した場合
    const { id } = item
    handler.handleDeleteSuccess(id)
    // setItems((prevItems) => prevItems.filter((item2) => item2.id !== id))
  }

  const onFileNameClick = (e: SyntheticEvent): void => {
    e.preventDefault()
    setPromptOpen(true)
    // const newname = prompt('新しいファイル名を入力してください。')
    // if (newname && item.name !== newname) {
    //   onChangeNameSuccess(item.id, newname)
    // }
  }
  const handlePromptConfirm = (newName: string): void => {
    if (newName && item.name !== newName) {
      handler.handleChangeNameSuccess(item.id, newName)
    }
  }

  return (
    <li>
      <ul>
        <li>
          <input type='checkbox' />
        </li>
        <li>
          {' '}
          <span>{item.type === 'file' ? '📄' : '📁'}</span>
        </li>
        <li>
          <span
            onContextMenu={onFileNameClick}
            onDoubleClick={(): void => {
              if (item.type === 'folder') {
                handler.setCurrentFolderId(item.id)
              }
            }}
          >
            <PromptModal
              isOpen={isPromptOpen}
              onClose={(): void => setPromptOpen(false)}
              onConfirm={handlePromptConfirm}
            />
            {item.name}
          </span>
        </li>
        <li>
          {' '}
          <span>{item.lastUpdated.toLocaleString()}</span>
        </li>
        <li>
          <span>{item.size} KB</span>
        </li>
        <li>
          <span className={FileItemsVersion}>{item.version}</span>
        </li>
        <li>
          <span>{item.updatedBy}</span>
        </li>
        <li>
          <button type='button'>ダウンロード</button>
        </li>
        <li>
          <UploadButton id={item.id} name={item.name} handleUploadSuccess={handler.handleUploadSuccess} />{' '}
        </li>
        <li>
          <button type='button' onClick={onDeleteClick}>
            削除
          </button>
        </li>
      </ul>
    </li>
  )
}

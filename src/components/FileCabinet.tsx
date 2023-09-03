import { css } from '@acab/ecsstatic/scss'
import { useEffect } from 'react'
import sleep from '../utils/common'
import { FileOrFolder, FileOrFolderItem } from './fileOrFolderItem'
import { useFileCabinet } from './useFileCabinet'

type Props = { initialFolderId: string }

const ListStyle = css`
  > li {
    height: 3rem;
    border-bottom: 1px solid red;
    display: grid;
    align-items: center;
    height: 100%;
    ul {
      display: grid;
      place-content: center;
      place-items: center;
      justify-items: center;
      align-items: center;
      gap: 1px;
      grid-template-columns:
        20px 20px minmax(200px, 1fr) 200px 150px 50px 150px minmax(50px, 100px)
        minmax(50px, 100px)
        minmax(50px, 100px);
    }
  }
`

function FileCabinet({ initialFolderId }: Props): JSX.Element {
  const { items, setItems, currentFolderId, handler } = useFileCabinet(initialFolderId)

  useEffect(() => {
    // GASからファイル・フォルダ情報を取得する関数を想定
    async function fetchData(folderId: string): Promise<void> {
      console.log(folderId)
      // ここにGASとの通信処理を書く
      // 例: const response = await fetch(`YOUR_GAS_URL?folderId=${folderId}`);
      // const data = await response.json();
      // setItems(data);
      await sleep(1)
      const data: FileOrFolder[] = [
        {
          id: '1',
          name: 'document1.txt',
          type: 'file',
          lastUpdated: '2023-08-19T12:00:00Z',
          size: 500,
          version: '1.0',
          updatedBy: 'userA',
        },
        {
          id: '2',
          name: 'document2.pdf',
          type: 'file',
          lastUpdated: '2023-08-18T10:30:00Z',
          size: 1500,
          version: '1.2',
          updatedBy: 'userB',
        },
        {
          id: '3',
          name: 'document3.docx',
          type: 'file',
          lastUpdated: '2023-08-17T14:20:00Z',
          size: 2000,
          version: '2.0',
          updatedBy: 'userC',
        },
        {
          id: '4',
          name: 'document4.xlsx',
          type: 'file',
          lastUpdated: '2023-08-16T09:15:00Z',
          size: 1000,
          version: '1.5',
          updatedBy: 'userA',
        },
        {
          id: '5',
          name: 'subfolder',
          type: 'folder',
          lastUpdated: '2023-08-15T16:45:00Z',
          size: 0,
          version: '1.0',
          updatedBy: 'userD',
        },
      ]

      setItems(data)
    }

    fetchData(currentFolderId).catch((error) => {
      console.error('An error occurred:', error)
    })
  }, [currentFolderId, setItems])

  return (
    <section>
      <h2>フォルダ名（実際にはAPIから取得）</h2>
      <ul className={ListStyle}>
        {items.map((item: FileOrFolder) => (
          <FileOrFolderItem
            item={item}
            handler={handler}
            // onFolderDoubleClick={handler.setCurrentFolderId}
            // onUploadClick={(): void => uploadSuccess(setItems)(item.id, item.version + 1)}
            // // onDeleteSuccess={(): void => deleteSuccess(setItems)(item.id)}
            // onChangeNameSuccess={handler.handleChangeNameSuccess}
          />
        ))}
      </ul>
    </section>
  )
}

export default FileCabinet

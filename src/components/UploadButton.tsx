import { css } from '@acab/ecsstatic/scss'
import { useState } from 'react'
import viteLogo from '../assets/download.svg'
import sleep from '../utils/common'
import type { HandleToggleLoadingResult } from './useFileCabinet'

const logo = css`
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 0.6em 1.2em;
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;

  cursor: pointer;
  transition: border-color 0.25s;

  &:hover {
    border-color: #646cff;
  }
  &:focus,
  &:focus-visible {
    outline: 4px auto -webkit-focus-ring-color;
  }
  img {
    height: 1em;
    will-change: filter;
    transition: filter 300ms;
  }
`

interface Props {
  id: string
  name: string
  handleUploadSuccess: (fileId: string, newVersion: string) => void
}

// function asyncHelper(func: () => Promise<void>): () => void {
//   return (): void => {
//     func()
//       .then(() => {
//         // 成功時の処理（必要であれば）
//       })
//       .catch((error) => {
//         console.error(error)
//       })
//   }
// }
function useToggleLoading({ id, name, handleUploadSuccess }: Props): HandleToggleLoadingResult {
  const [isLoading, setIsLoading] = useState(false)
  const onClick = async (): Promise<void> => {
    setIsLoading(true) // ボタンを「ローディング」状態にする
    try {
      handleUploadSuccess(id, name) // 時間のかかる処理
      await sleep(2000)
    } catch (error) {
      console.error('An error occurred:', error)
    }
    setIsLoading(false) // ボタンを「非ローディング」状態に戻す
  }
  return { isLoading, onClick }
}

function UploadButton({ id, name, handleUploadSuccess }: Props): JSX.Element {
  const { isLoading, onClick } = useToggleLoading({ id, name, handleUploadSuccess })
  return (
    <button type='button' className={logo} onClick={onClick} disabled={isLoading}>
      {isLoading ? 'Uploading...' : <img src={viteLogo} alt='Vite logo' />}
    </button>
  )
}

export default UploadButton

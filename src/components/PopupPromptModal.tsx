import { useState } from 'react'

type Props = {
  isOpen: boolean
  onClose: () => void
  onConfirm: (inputValue: string) => void
}
function PopupPromptModal({ isOpen, onClose, onConfirm }: Props): JSX.Element | null {
  const [inputValue, setInputValue] = useState('')

  const handleConfirm = (): void => {
    onConfirm(inputValue)
    onClose()
  }

  if (!isOpen) return null

  return (
    <dialog className='modal'>
      <div className='modal-content'>
        <h4>新しいファイル名を入力してください。</h4>
        <input type='text' value={inputValue} onChange={(e): void => setInputValue(e.target.value)} />
        <button type='button' onClick={onClose}>
          キャンセル
        </button>
        <button type='button' onClick={handleConfirm}>
          OK
        </button>
      </div>
    </dialog>
  )
}

export default PopupPromptModal

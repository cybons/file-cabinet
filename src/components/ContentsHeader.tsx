import { useState } from 'react'
import { asString } from '../utils/stringUtils'

function HeaderTypeA(): JSX.Element {
  return <div>Header Type A</div>
}
function HeaderTypeB(): JSX.Element {
  return <div>Header Type B</div>
}
function HeaderTypeC(): JSX.Element {
  return <div>Header Type C</div>
}

export function MainContainer(): JSX.Element {
  const [headerType, setHeaderType] = useState('A') // デフォルトはタイプA

  const renderHeader = (): JSX.Element | null => {
    switch (headerType) {
      case 'A':
        return <HeaderTypeA />
      case 'B':
        return <HeaderTypeB />
      case 'C':
        return <HeaderTypeC />
      default:
        return null
    }
  }

  const onClick = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>): void => {
    const id = asString(e.currentTarget.dataset.id)
    setHeaderType(id)
  }

  return (
    <div className='contants-header'>
      <button type='button' data-id='A' onClick={onClick}>
        Type A
      </button>
      <button type='button' data-id='B' onClick={onClick}>
        Type B
      </button>
      <button type='button' data-id='C' onClick={onClick}>
        Type C
      </button>
      {renderHeader()}
      {/* ここにmainContainerの内容 */}
    </div>
  )
}

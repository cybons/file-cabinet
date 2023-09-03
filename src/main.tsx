import { css } from '@acab/ecsstatic/scss'
import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './components/App'
import { MainContainer } from './components/ContentsHeader'
import FileCabinet from './components/FileCabinet'
import './styles/reset.css'

type Prop = { text: string }

const button = css`
  // ...
  color: #1004ff;

  &:hover,
  &:focus {
    color: red;
  }
`

function Button({ text }: Prop): JSX.Element {
  return (
    <button type='button' className={button}>
      {text}
    </button>
  )
}

const root = document.getElementById('root')
if (root) {
  console.log(root?.append('1'))
  const re = createRoot(root)
  re.render(
    <React.StrictMode>
      <App />
      <Button text='aaaa' />
    </React.StrictMode>,
  )
}

function HelloMessage(): JSX.Element {
  return (
    <div>
      Hello World<p>aaaa</p>
    </div>
  )
}

const container = document.getElementById('root')
if (container) {
  const root2 = createRoot(container)
  root2.render(
    <React.StrictMode>
      <FileCabinet initialFolderId='root' />
      <HelloMessage />
      <MainContainer />
    </React.StrictMode>,
  )
}

export default Button

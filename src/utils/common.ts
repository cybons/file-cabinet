/**
 * 指定時間処理を停止する関数
 * @param {number} ms 待機するミリ秒数
 */
async function sleep(ms: number): Promise<unknown> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms)
  })
}

export default sleep

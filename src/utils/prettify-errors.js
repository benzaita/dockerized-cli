module.exports = fn => argv => {
  try {
    fn(argv)
  } catch (e) {
    console.error(e.message)
    process.exit(1)
  }
}

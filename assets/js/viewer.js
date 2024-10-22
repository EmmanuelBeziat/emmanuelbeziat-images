class Viewer {
	constructor (elements) {
		this.links = elements

		if (!this.links) return
		this.links.forEach(link => {
			this.handleClick(link)
		})
	}

	handleClick (link) {
		link.addEventListener('click', event => {
			event.preventDefault()
			const url = event.target.href
			navigator.clipboard.writeText(url)
				.then(() => {
					tippy('#myButton', {
						content: 'URL Copiée',
						arrow: false,
						delay: [100, 2000]
					})
				})
				.catch(err => {
					tippy('#myButton', {
						content: err.message,
						arrow: false,
						delay: [100, 2000]
					})
				})
		})
	}
}

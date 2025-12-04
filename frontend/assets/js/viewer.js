class Viewer {
	constructor (elements) {
		this.links = elements

		if (!this.links || !this.links.length) return
		this.links.forEach(link => this.handleClick(link))
	}

	handleClick (link) {
		link.addEventListener('click', event => {
			event.preventDefault()
			const url = link.href

			navigator.clipboard.writeText(url)
				.then(() => {
					if (window.tippy) {
						const tip = link._tippy || window.tippy(link, {
							trigger: 'manual',
							arrow: false,
							placement: 'bottom',
							hideOnClick: false
						})
						tip.setContent('URL copiée')
						tip.show()
						setTimeout(() => tip.hide(), 1500)
					}
				})
				.catch(err => {
					if (window.tippy) {
						const tip = link._tippy || window.tippy(link, {
							trigger: 'manual',
							arrow: false,
							placement: 'bottom',
							hideOnClick: false
						})
						tip.setContent(err.message)
						tip.show()
						setTimeout(() => tip.hide(), 2000)
					}
				})
		})
	}
}

// Expose global for inline usage in HTML
if (typeof window !== 'undefined') {
	window.Viewer = Viewer
}

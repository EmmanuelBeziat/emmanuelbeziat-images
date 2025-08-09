import js from "@eslint/js"
import globals from "globals"
import { defineConfig } from "eslint/config"

export default defineConfig([
  {
		ignores: [
			"**/node_modules/**",
			"**/dist/**",
			"**/vendors/**",
			"**/tests/**"
		]
	},
  {
		files: ["**/*.{js,mjs,cjs}"],
		plugins: { js },
		extends: ["js/recommended"],
		rules: {
			'no-tabs': 'off',
			'brace-style': [
				'error',
				'stroustrup'
			],
			'comma-dangle': [
				'error',
				'only-multiline'
			],
			'no-unused-vars': [
				'error', {
					'argsIgnorePattern': '^_'
				}
			]
		}
	},
	{
		languageOptions: {
			globals: {
				...globals.node, ...globals.browser
			}
		}
	}
])

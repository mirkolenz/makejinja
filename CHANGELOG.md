# Changelog

## [0.7.5](https://github.com/mirkolenz/makejinja/compare/v0.7.4...v0.7.5) (2022-12-30)


### Bug Fixes

* **deps:** update dependency rich to v13 ([#11](https://github.com/mirkolenz/makejinja/issues/11)) ([86b15d7](https://github.com/mirkolenz/makejinja/commit/86b15d7325c9cc4e50f69cad6c3fd5628a242817))

## [1.0.0-beta.2](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.1...v1.0.0-beta.2) (2022-12-28)


### Features

* add options to change jinja delimiters ([edd1caa](https://github.com/mirkolenz/makejinja/commit/edd1caac1b1cd22d14d0bd59aa33061934b1a25b))

## [1.0.0-beta.1](https://github.com/mirkolenz/makejinja/compare/v0.7.4...v1.0.0-beta.1) (2022-12-26)


### ⚠ BREAKING CHANGES

* Massive performance boost over python-simpleconf. The CLI options changed: env-vars are no longer supported and we only handle files ending in `yaml` or `yml`.

### Features

* add checks to verify correct file handling ([5d5d5fd](https://github.com/mirkolenz/makejinja/commit/5d5d5fdd3473efebf41fbad83891786f9e902688))
* switch to pure yaml config parsing ([ac22a0d](https://github.com/mirkolenz/makejinja/commit/ac22a0df5e1a6bd48bda457e797b271aa9b9aae5))


### Bug Fixes

* improve cli output ([1280fa7](https://github.com/mirkolenz/makejinja/commit/1280fa71c83af483419c6e0c58f3e5c4757c5c3c))

## [0.7.4](https://github.com/mirkolenz/makejinja/compare/v0.7.3...v0.7.4) (2022-12-18)


### Bug Fixes

* bump version ([2a80893](https://github.com/mirkolenz/makejinja/commit/2a808933a75cfdb5af5e2e4b6c1b982304ce1a9d))

## [0.7.3](https://github.com/mirkolenz/makejinja/compare/v0.7.2...v0.7.3) (2022-12-18)


### Bug Fixes

* bump version ([ab04f19](https://github.com/mirkolenz/makejinja/commit/ab04f19714dfaaa2a44f7f37cb726744b184dd7b))

## [0.7.2](https://github.com/mirkolenz/makejinja/compare/v0.7.1...v0.7.2) (2022-12-18)


### Bug Fixes

* bump version ([0a6611a](https://github.com/mirkolenz/makejinja/commit/0a6611ab6699891acbacb2fbd8488aeec6cc3122))

## [0.7.1](https://github.com/mirkolenz/makejinja/compare/v0.7.0...v0.7.1) (2022-12-18)


### Bug Fixes

* wrong loading of env vars data ([4bd764b](https://github.com/mirkolenz/makejinja/commit/4bd764b85b09985ce1990ac90147f084394d3a9f))

## [0.7.0](https://github.com/mirkolenz/makejinja/compare/v0.6.0...v0.7.0) (2022-12-17)


### Features

* add documentation to cli ([b001d04](https://github.com/mirkolenz/makejinja/commit/b001d04c0a622b3012e7a6d587be171d22331d12))


### Bug Fixes

* improve command output ([36df06f](https://github.com/mirkolenz/makejinja/commit/36df06fecc14b443a452e2f2e49107870fb517d9))
* process env vars after files ([31cb946](https://github.com/mirkolenz/makejinja/commit/31cb946b5ad47beed2788e53d4b39c50fe7da256))
* sort files in iterdir ([5be3db1](https://github.com/mirkolenz/makejinja/commit/5be3db18898fe868d45fea6cfdab6ba3fe6bbbf3))

## [0.6.0](https://github.com/mirkolenz/makejinja/compare/v0.5.1...v0.6.0) (2022-12-15)


### Features

* update cli param names ([c819a51](https://github.com/mirkolenz/makejinja/commit/c819a51d309803fb8e6a56d9ba6d52334b79bda0))


### Documentation

* update readme ([dd3eec7](https://github.com/mirkolenz/makejinja/commit/dd3eec77ffc96f1cc544013c4ada4e4663bbe7b7))

## [0.5.1](https://github.com/mirkolenz/makejinja/compare/v0.5.0...v0.5.1) (2022-12-14)


### Bug Fixes

* enable file-based loading of globals & filters ([cf9f331](https://github.com/mirkolenz/makejinja/commit/cf9f331f81c13cc8d2834f5c748776d7d332fd4d))

## [0.5.0](https://github.com/mirkolenz/makejinja/compare/v0.4.1...v0.5.0) (2022-12-14)


### Features

* allow customization of globals and filters ([d86bd5a](https://github.com/mirkolenz/makejinja/commit/d86bd5a195b0e8ace992f28e13bb0c13f4bcea42))

## [0.4.1](https://github.com/mirkolenz/makejinja/compare/v0.4.0...v0.4.1) (2022-12-14)


### Bug Fixes

* handle empty templates with newlines ([97123b6](https://github.com/mirkolenz/makejinja/commit/97123b6f20ac608edd42962b4f031ef967c8e5df))

## [0.4.0](https://github.com/mirkolenz/makejinja/compare/v0.3.0...v0.4.0) (2022-12-14)


### Features

* add skip-entry cli param ([7d79fa9](https://github.com/mirkolenz/makejinja/commit/7d79fa95c2411aced7d7085d5d385b8f594cbd55))

## [0.3.0](https://github.com/mirkolenz/makejinja/compare/v0.2.1...v0.3.0) (2022-12-14)


### Features

* add global function to select a language ([b26836d](https://github.com/mirkolenz/makejinja/commit/b26836df42f87af42a5145cd2ddfd3e61f8e5dd9))

## [0.2.1](https://github.com/mirkolenz/makejinja/compare/v0.2.0...v0.2.1) (2022-12-11)


### Bug Fixes

* improve compatability with python 3.9 ([30919e8](https://github.com/mirkolenz/makejinja/commit/30919e83e11fbc368b8d97d498dab7ae2e766671))

## v0.2.0 (2022-12-11)

### Feature

- Add option to remove jinja suffix after rendering ([`d1ec7d6`](https://github.com/mirkolenz/makejinja/commit/d1ec7d6079ec3cf2e124a708dfe5688284add192))

### Documentation

- Fix changelog ([`cfab1b4`](https://github.com/mirkolenz/makejinja/commit/cfab1b436036caae98a11798b98adc857f8fa189))

## [v0.1.1](https://github.com/mirkolenz/makejinja/compare/0.1.0...0.1.1) (2022-12-10)

### Bug Fixes

- change script name to makejinja ([df14627](https://github.com/mirkolenz/makejinja/commit/df14627056c40e62adc489ac4c766b796e59f34f))

## v0.1.0 (2022-12-10)

- Initial release

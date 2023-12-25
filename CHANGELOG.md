# Changelog

## [2.3.2](https://github.com/mirkolenz/makejinja/compare/v2.3.1...v2.3.2) (2023-11-08)


### Bug Fixes

* trigger release ([a331675](https://github.com/mirkolenz/makejinja/commit/a33167527ff887e6d77c40459b1ccb92b6ece964))

## [2.3.1](https://github.com/mirkolenz/makejinja/compare/v2.3.0...v2.3.1) (2023-11-08)


### Bug Fixes

* update links in readme ([8dfe58e](https://github.com/mirkolenz/makejinja/commit/8dfe58e2c58872d70a5b93d0b3a34d473a3382a8))

## [2.3.0](https://github.com/mirkolenz/makejinja/compare/v2.2.0...v2.3.0) (2023-11-06)


### Features

* add flag to pass key-value options via cli ([c59e76f](https://github.com/mirkolenz/makejinja/commit/c59e76fa966cdf2cfca9b39ab5ea15cddc15e030))
* add force option to enable overwriting ([a9adedc](https://github.com/mirkolenz/makejinja/commit/a9adedcee0ddbcad3fd5e6ab0db55e31c7622f08))
* add quiet option to silence output ([78b6b44](https://github.com/mirkolenz/makejinja/commit/78b6b448d91973f0619807098cf6216fca4414fd))
* add shorthand values for cli options ([dd033c2](https://github.com/mirkolenz/makejinja/commit/dd033c2e841d5ab5e780722ba338e4e8ffbe04ee))
* allow files to be passed as inputs ([b78fa4b](https://github.com/mirkolenz/makejinja/commit/b78fa4bc63c1cecf2db69782df1476189f8d50f5))
* allow output to be a file in certain cases ([c85763f](https://github.com/mirkolenz/makejinja/commit/c85763f95394f378b9b72a76b8179565dbc62858))
* optimize data handling (update globals) ([1016fe9](https://github.com/mirkolenz/makejinja/commit/1016fe94d510b7cf4dae99760ab923800a85ce10))
* pass os.environ to globals ([c9f646c](https://github.com/mirkolenz/makejinja/commit/c9f646c6571b95b5dbe6b3746c1b48a03db1744f))
* require using a flag to remove the output directory ([f0b288d](https://github.com/mirkolenz/makejinja/commit/f0b288d3fc15fcf23455f3b8434a0a2c87aed5a9))
* update loader to better support globals ([c38b564](https://github.com/mirkolenz/makejinja/commit/c38b564b4ccbd4543975e18fa4e0f1cc1eec3d10))


### Bug Fixes

* add shorthand options for version/help ([e4f1cf0](https://github.com/mirkolenz/makejinja/commit/e4f1cf01c24ab121a9dfa6c01869db1f278c835d))
* do not enforce jinja suffix for input files ([152d220](https://github.com/mirkolenz/makejinja/commit/152d220b4b8d274c6ea638731ed50adfa65ba92c))
* pass immutable data to loader ([1351f2c](https://github.com/mirkolenz/makejinja/commit/1351f2c4a39af7b082fbd8c0c0e7cc804569aa6a))
* rename clean-output to clean ([523556c](https://github.com/mirkolenz/makejinja/commit/523556cc3d63afa9008037db2990a37e222bff7f))
* update cli option groups ([380d0db](https://github.com/mirkolenz/makejinja/commit/380d0db3218ba3d41460f68bb6e2aa1f672b168e))

## [2.2.0](https://github.com/mirkolenz/makejinja/compare/v2.1.4...v2.2.0) (2023-11-03)


### Features

* allow customization of undefined behavior ([fd84618](https://github.com/mirkolenz/makejinja/commit/fd846189f4e9702c5f08dc344abb3dff062b1a5d))

## [2.1.4](https://github.com/mirkolenz/makejinja/compare/v2.1.3...v2.1.4) (2023-11-03)


### Bug Fixes

* update description of project ([2f4e405](https://github.com/mirkolenz/makejinja/commit/2f4e40563350d4eb12912db9bdb0e19b4231a791))

## [2.1.3](https://github.com/mirkolenz/makejinja/compare/v2.1.2...v2.1.3) (2023-11-03)


### Bug Fixes

* use correct ref for building docs ([b7e30f7](https://github.com/mirkolenz/makejinja/commit/b7e30f773c2bd18e29333ba654ee7a3cdc85e07d))

## [2.1.2](https://github.com/mirkolenz/makejinja/compare/v2.1.1...v2.1.2) (2023-11-03)


### Bug Fixes

* trigger release ([fd6579d](https://github.com/mirkolenz/makejinja/commit/fd6579d7650889843f10699999bce2cef4c18f53))

## [2.1.1](https://github.com/mirkolenz/makejinja/compare/v2.1.0...v2.1.1) (2023-10-31)


### Bug Fixes

* expose cli module in main init ([ed429a0](https://github.com/mirkolenz/makejinja/commit/ed429a0b61814bbd35a7ab36014e556c65dec597))

## [2.1.0](https://github.com/mirkolenz/makejinja/compare/v2.0.2...v2.1.0) (2023-10-30)


### Features

* add data handler for json files ([d18f514](https://github.com/mirkolenz/makejinja/commit/d18f514a0722fbbea3886d538deec45470207d68))


### Bug Fixes

* require at least python 3.11 and drop tomli ([ebdeb64](https://github.com/mirkolenz/makejinja/commit/ebdeb64c765eefcb250c541c46167059af0c154e))

## [2.0.2](https://github.com/mirkolenz/makejinja/compare/v2.0.1...v2.0.2) (2023-10-26)


### Bug Fixes

* use poetry2nix again after upstream fixes ([3b7dac0](https://github.com/mirkolenz/makejinja/commit/3b7dac03faf7418d0eb78cd5ed3f3f970235b0cb))

## [2.0.1](https://github.com/mirkolenz/makejinja/compare/v2.0.0...v2.0.1) (2023-09-30)


### Bug Fixes

* bump deps ([193f396](https://github.com/mirkolenz/makejinja/commit/193f396a233d77cf1390622819990563f3055162))
* remove default command from docker image ([c562377](https://github.com/mirkolenz/makejinja/commit/c5623773947d602f7892bef5c8723a5f03da5c4e))

## [2.0.0](https://github.com/mirkolenz/makejinja/compare/v1.1.5...v2.0.0) (2023-06-18)


### ⚠ BREAKING CHANGES

* The configuration file has been renamed from `.makejinja.toml` to `makejinja.toml`. Please rename your files accordingly.
* The parameter `input_pattern` has been changed to `include_patterns` which now accepts a list of patterns.
* In this version, `input` has been removed an replaced with `inputs` (allowing to use multiple input folders). We also included a new option `exclude_patterns` to ignore files that would be matched by `input_pattern`. The option `copy_tree` is superseded by the new `copy_metadata` which is compatible with multiple inputs and preserves attributes for rendered files as well. Please adjust your config accordingly, otherwise `makejinja` will break!

### Features

* add version option ([0585114](https://github.com/mirkolenz/makejinja/commit/058511497517724d6e37bd8e4054a16641476366))
* completely rewrite file handling ([#20](https://github.com/mirkolenz/makejinja/issues/20)) ([97d6a51](https://github.com/mirkolenz/makejinja/commit/97d6a51d268689bd50fa1b4a9a70c099db42bda4))
* remove leading dot from config file ([4742165](https://github.com/mirkolenz/makejinja/commit/4742165ed4e18c67543f5c46411989d752e867f9))
* rename input_pattern to include_patterns ([21e3e85](https://github.com/mirkolenz/makejinja/commit/21e3e85d91cb0c2c2426bd36137998e36c5140ef))


### Bug Fixes

* add multi-arch docker images ([6024633](https://github.com/mirkolenz/makejinja/commit/6024633e84a895eeb9cb2db0860cfa0bd77b7954))
* apply exclude patterns to files and folders ([5d80747](https://github.com/mirkolenz/makejinja/commit/5d807474276b107047422f1430bbb890f9cb9d7d))
* provide aarch64 docker image ([e983268](https://github.com/mirkolenz/makejinja/commit/e983268df920741921384d4ea4f75f92f79f524e))
* remove aarch64 docker image due to bugs ([0af11a2](https://github.com/mirkolenz/makejinja/commit/0af11a24c24dc7200253f9864126bda14a9ebf29))
* update nix flake ([05b9575](https://github.com/mirkolenz/makejinja/commit/05b95756e2682f4acad69f7ebbbcfd75eb945a02))

## [2.0.0-beta.8](https://github.com/mirkolenz/makejinja/compare/v2.0.0-beta.7...v2.0.0-beta.8) (2023-06-13)


### ⚠ BREAKING CHANGES

* The configuration file has been renamed from `.makejinja.toml` to `makejinja.toml`. Please rename your files accordingly.
* The parameter `input_pattern` has been changed to `include_patterns` which now accepts a list of patterns.

### Features

* remove leading dot from config file ([4742165](https://github.com/mirkolenz/makejinja/commit/4742165ed4e18c67543f5c46411989d752e867f9))
* rename input_pattern to include_patterns ([21e3e85](https://github.com/mirkolenz/makejinja/commit/21e3e85d91cb0c2c2426bd36137998e36c5140ef))

## [2.0.0-beta.7](https://github.com/mirkolenz/makejinja/compare/v2.0.0-beta.6...v2.0.0-beta.7) (2023-06-13)


### Bug Fixes

* add multi-arch docker images ([6024633](https://github.com/mirkolenz/makejinja/commit/6024633e84a895eeb9cb2db0860cfa0bd77b7954))

## [2.0.0-beta.6](https://github.com/mirkolenz/makejinja/compare/v2.0.0-beta.5...v2.0.0-beta.6) (2023-06-01)


### Bug Fixes

* apply exclude patterns to files and folders ([5d80747](https://github.com/mirkolenz/makejinja/commit/5d807474276b107047422f1430bbb890f9cb9d7d))

## [2.0.0-beta.5](https://github.com/mirkolenz/makejinja/compare/v2.0.0-beta.4...v2.0.0-beta.5) (2023-05-25)


### Bug Fixes

* remove aarch64 docker image due to bugs ([0af11a2](https://github.com/mirkolenz/makejinja/commit/0af11a24c24dc7200253f9864126bda14a9ebf29))

## [2.0.0-beta.4](https://github.com/mirkolenz/makejinja/compare/v2.0.0-beta.3...v2.0.0-beta.4) (2023-05-25)


### Bug Fixes

* update nix flake ([05b9575](https://github.com/mirkolenz/makejinja/commit/05b95756e2682f4acad69f7ebbbcfd75eb945a02))

## [2.0.0-beta.3](https://github.com/mirkolenz/makejinja/compare/v2.0.0-beta.2...v2.0.0-beta.3) (2023-05-25)


### Bug Fixes

* provide aarch64 docker image ([e983268](https://github.com/mirkolenz/makejinja/commit/e983268df920741921384d4ea4f75f92f79f524e))

## [2.0.0-beta.2](https://github.com/mirkolenz/makejinja/compare/v2.0.0-beta.1...v2.0.0-beta.2) (2023-05-24)


### Features

* add version option ([0585114](https://github.com/mirkolenz/makejinja/commit/058511497517724d6e37bd8e4054a16641476366))

## [2.0.0-beta.1](https://github.com/mirkolenz/makejinja/compare/v1.1.5...v2.0.0-beta.1) (2023-05-18)


### ⚠ BREAKING CHANGES

* In this version, `input` has been removed an replaced with `inputs` (allowing to use multiple input folders). We also included a new option `exclude_patterns` to ignore files that would be matched by `input_pattern`. The option `copy_tree` is superseded by the new `copy_metadata` which is compatible with multiple inputs and preserves attributes for rendered files as well. Please adjust your config accordingly, otherwise `makejinja` will break!

### Features

* completely rewrite file handling ([#20](https://github.com/mirkolenz/makejinja/issues/20)) ([97d6a51](https://github.com/mirkolenz/makejinja/commit/97d6a51d268689bd50fa1b4a9a70c099db42bda4))

## [1.1.5](https://github.com/mirkolenz/makejinja/compare/v1.1.4...v1.1.5) (2023-05-17)


### Bug Fixes

* trigger ci build ([acd7609](https://github.com/mirkolenz/makejinja/commit/acd7609c4cdfaf546e4d28eee14642a8e9f580e5))
* try to fix docker image pushing ([6634507](https://github.com/mirkolenz/makejinja/commit/663450742507ba308082d4f7e17b4e71c0f4ee23))
* update readme ([2445d25](https://github.com/mirkolenz/makejinja/commit/2445d254cc6cde9953ebe8055a1c97640f01527e))
* use impure nix run for pushing docker ([634f699](https://github.com/mirkolenz/makejinja/commit/634f699d3b68060d1265c47e044f993977028257))

## [1.1.5-beta.4](https://github.com/mirkolenz/makejinja/compare/v1.1.5-beta.3...v1.1.5-beta.4) (2023-05-09)


### Bug Fixes

* update readme ([2445d25](https://github.com/mirkolenz/makejinja/commit/2445d254cc6cde9953ebe8055a1c97640f01527e))

## [1.1.5-beta.3](https://github.com/mirkolenz/makejinja/compare/v1.1.5-beta.2...v1.1.5-beta.3) (2023-05-09)


### Bug Fixes

* use impure nix run for pushing docker ([634f699](https://github.com/mirkolenz/makejinja/commit/634f699d3b68060d1265c47e044f993977028257))

## [1.1.5-beta.2](https://github.com/mirkolenz/makejinja/compare/v1.1.5-beta.1...v1.1.5-beta.2) (2023-05-09)


### Bug Fixes

* try to fix docker image pushing ([6634507](https://github.com/mirkolenz/makejinja/commit/663450742507ba308082d4f7e17b4e71c0f4ee23))

## [1.1.5-beta.1](https://github.com/mirkolenz/makejinja/compare/v1.1.4...v1.1.5-beta.1) (2023-05-08)


### Bug Fixes

* trigger ci build ([acd7609](https://github.com/mirkolenz/makejinja/commit/acd7609c4cdfaf546e4d28eee14642a8e9f580e5))

## [1.1.4](https://github.com/mirkolenz/makejinja/compare/v1.1.3...v1.1.4) (2023-04-30)


### Bug Fixes

* trigger ci build ([f529ff0](https://github.com/mirkolenz/makejinja/commit/f529ff0f323941dc0bafb2366c768f1a316ae293))

## [1.1.3](https://github.com/mirkolenz/makejinja/compare/v1.1.2...v1.1.3) (2023-04-30)


### Bug Fixes

* help message was missing from cli ([34b626e](https://github.com/mirkolenz/makejinja/commit/34b626e52ff32ee6ce2dbba8351877441d1c9903))

## [1.1.2](https://github.com/mirkolenz/makejinja/compare/v1.1.1...v1.1.2) (2023-02-14)


### Bug Fixes

* **loader:** remove protocol to enable subclassing ([db55ae3](https://github.com/mirkolenz/makejinja/commit/db55ae36478ddd7899ad6fc0395f3f84e796e637))

## [1.1.1](https://github.com/mirkolenz/makejinja/compare/v1.1.0...v1.1.1) (2023-02-14)


### Bug Fixes

* use protocol instead of abc for loader class ([d72bec1](https://github.com/mirkolenz/makejinja/commit/d72bec10bf555d9aca53e712195171253ee3f003))

## [1.1.0](https://github.com/mirkolenz/makejinja/compare/v1.0.1...v1.1.0) (2023-02-06)


### Features

* enable programmatic usage of the library ([ddc744b](https://github.com/mirkolenz/makejinja/commit/ddc744bd4427c6d7480f6c45b10b6ab329e24b90))


### Bug Fixes

* add all annotations to config/loader ([6070e5a](https://github.com/mirkolenz/makejinja/commit/6070e5aca09adc07998dfa7240544badfd116331))
* add py.typed file ([3756882](https://github.com/mirkolenz/makejinja/commit/3756882401b6e2402715b5ddaf484a8b3a3c5ecc))
* modularize app, improve loader construction ([a8da7fa](https://github.com/mirkolenz/makejinja/commit/a8da7fac03a08ba23ca9a7debc9c183fc7688ce6))

## [1.0.1](https://github.com/mirkolenz/makejinja/compare/v1.0.0...v1.0.1) (2023-02-03)


### Bug Fixes

* **docker:** use entrypoint for proper cli usage ([fcebe4d](https://github.com/mirkolenz/makejinja/commit/fcebe4de622bbbc654ee2799a94affb515a4ab30))

## [1.0.0](https://github.com/mirkolenz/makejinja/compare/v0.7.5...v1.0.0) (2023-01-25)


### ⚠ BREAKING CHANGES

* use jinja methods to import custom loaders
* enhance support for custom loaders
* rename input/output options
* enhance custom code & remove cli options
* switch from typer to click & typed-settings
* Massive performance boost over python-simpleconf. The CLI options changed: env-vars are no longer supported and we only handle files ending in `yaml` or `yml`.

### Features

* add checks to verify correct file handling ([5d5d5fd](https://github.com/mirkolenz/makejinja/commit/5d5d5fdd3473efebf41fbad83891786f9e902688))
* add initial support to load custom code ([9404ecc](https://github.com/mirkolenz/makejinja/commit/9404eccca2db01858242d2f445b814311188ba07))
* add options to change jinja delimiters ([edd1caa](https://github.com/mirkolenz/makejinja/commit/edd1caac1b1cd22d14d0bd59aa33061934b1a25b))
* add python data loader ([2a0b817](https://github.com/mirkolenz/makejinja/commit/2a0b8170f68e8e6a3658ff3c1bd79e7eeab4841b))
* collect modules in subfolders ([ebfa242](https://github.com/mirkolenz/makejinja/commit/ebfa24230ca8056ad2ed2194f69530c6ff93a80b))
* enhance custom code & remove cli options ([a8b0b64](https://github.com/mirkolenz/makejinja/commit/a8b0b641304583377975d9960d0677596ad88709))
* enhance support for custom loaders ([46c8eb1](https://github.com/mirkolenz/makejinja/commit/46c8eb1eda830f36f1d0d657adfe28046a0b82fe))
* pass jinja options to env constructor ([f39fe32](https://github.com/mirkolenz/makejinja/commit/f39fe32c61ef100241b58b14e9d53ba11ab20356))
* rename input/output options ([2592c19](https://github.com/mirkolenz/makejinja/commit/2592c196fce2fd872e76c86d902f3322d6c5d02c))
* switch from typer to click & typed-settings ([3e9d09d](https://github.com/mirkolenz/makejinja/commit/3e9d09d53c1a68fb47a40c25b088809198f30e10))
* switch to pure yaml config parsing ([ac22a0d](https://github.com/mirkolenz/makejinja/commit/ac22a0df5e1a6bd48bda457e797b271aa9b9aae5))
* use jinja methods to import custom loaders ([901f37a](https://github.com/mirkolenz/makejinja/commit/901f37a35e9287fc1f0a98c9f3ccc23cafd3cbc5))


### Bug Fixes

* add missing main package file ([b436dda](https://github.com/mirkolenz/makejinja/commit/b436dda408e04b510d3bd6185e29dd257029aa84))
* improve cli output ([1280fa7](https://github.com/mirkolenz/makejinja/commit/1280fa71c83af483419c6e0c58f3e5c4757c5c3c))
* improve options ([e81d727](https://github.com/mirkolenz/makejinja/commit/e81d727469d012579ec04fb1e61d28076ffe7a7e))
* improve types ([475e2a5](https://github.com/mirkolenz/makejinja/commit/475e2a54220998c5b1022f1b89228d42b04ccc91))
* make custom import paths more robust ([7424729](https://github.com/mirkolenz/makejinja/commit/7424729cdba1b168193fec72b9d0639c16962107))
* properly set pythonpath for module resolution ([6beb0b0](https://github.com/mirkolenz/makejinja/commit/6beb0b0a8bd4a7649dffd5f734805ae951c58841))
* remove wrong flag decls from click params ([5d98f08](https://github.com/mirkolenz/makejinja/commit/5d98f08752b264b94d9091755e3ad1ca515496c0))
* update typed-settings and remove type casts ([e42309d](https://github.com/mirkolenz/makejinja/commit/e42309de1020c4cd0463ec4948933b83caad9438))

## [1.0.0-beta.12](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.11...v1.0.0-beta.12) (2023-01-15)


### Bug Fixes

* make custom import paths more robust ([7424729](https://github.com/mirkolenz/makejinja/commit/7424729cdba1b168193fec72b9d0639c16962107))

## [1.0.0-beta.11](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.10...v1.0.0-beta.11) (2023-01-15)


### Bug Fixes

* properly set pythonpath for module resolution ([6beb0b0](https://github.com/mirkolenz/makejinja/commit/6beb0b0a8bd4a7649dffd5f734805ae951c58841))

## [1.0.0-beta.10](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.9...v1.0.0-beta.10) (2023-01-15)


### ⚠ BREAKING CHANGES

* use jinja methods to import custom loaders

### Features

* use jinja methods to import custom loaders ([901f37a](https://github.com/mirkolenz/makejinja/commit/901f37a35e9287fc1f0a98c9f3ccc23cafd3cbc5))


### Bug Fixes

* improve types ([475e2a5](https://github.com/mirkolenz/makejinja/commit/475e2a54220998c5b1022f1b89228d42b04ccc91))

## [1.0.0-beta.9](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.8...v1.0.0-beta.9) (2023-01-15)


### ⚠ BREAKING CHANGES

* enhance support for custom loaders

### Features

* enhance support for custom loaders ([46c8eb1](https://github.com/mirkolenz/makejinja/commit/46c8eb1eda830f36f1d0d657adfe28046a0b82fe))

## [1.0.0-beta.8](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.7...v1.0.0-beta.8) (2023-01-15)


### ⚠ BREAKING CHANGES

* rename input/output options

### Features

* collect modules in subfolders ([ebfa242](https://github.com/mirkolenz/makejinja/commit/ebfa24230ca8056ad2ed2194f69530c6ff93a80b))
* pass jinja options to env constructor ([f39fe32](https://github.com/mirkolenz/makejinja/commit/f39fe32c61ef100241b58b14e9d53ba11ab20356))
* rename input/output options ([2592c19](https://github.com/mirkolenz/makejinja/commit/2592c196fce2fd872e76c86d902f3322d6c5d02c))


### Bug Fixes

* improve options ([e81d727](https://github.com/mirkolenz/makejinja/commit/e81d727469d012579ec04fb1e61d28076ffe7a7e))

## [1.0.0-beta.7](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.6...v1.0.0-beta.7) (2023-01-14)


### ⚠ BREAKING CHANGES

* enhance custom code & remove cli options

### Features

* add initial support to load custom code ([9404ecc](https://github.com/mirkolenz/makejinja/commit/9404eccca2db01858242d2f445b814311188ba07))
* add python data loader ([2a0b817](https://github.com/mirkolenz/makejinja/commit/2a0b8170f68e8e6a3658ff3c1bd79e7eeab4841b))
* enhance custom code & remove cli options ([a8b0b64](https://github.com/mirkolenz/makejinja/commit/a8b0b641304583377975d9960d0677596ad88709))

## [1.0.0-beta.6](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.5...v1.0.0-beta.6) (2023-01-14)


### Bug Fixes

* add missing main package file ([b436dda](https://github.com/mirkolenz/makejinja/commit/b436dda408e04b510d3bd6185e29dd257029aa84))
* update typed-settings and remove type casts ([e42309d](https://github.com/mirkolenz/makejinja/commit/e42309de1020c4cd0463ec4948933b83caad9438))

## [1.0.0-beta.5](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.4...v1.0.0-beta.5) (2023-01-05)


### Bug Fixes

* remove wrong flag decls from click params ([5d98f08](https://github.com/mirkolenz/makejinja/commit/5d98f08752b264b94d9091755e3ad1ca515496c0))

## [1.0.0-beta.4](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.3...v1.0.0-beta.4) (2023-01-03)


### ⚠ BREAKING CHANGES

* switch from typer to click & typed-settings

### Features

* switch from typer to click & typed-settings ([3e9d09d](https://github.com/mirkolenz/makejinja/commit/3e9d09d53c1a68fb47a40c25b088809198f30e10))

## [1.0.0-beta.3](https://github.com/mirkolenz/makejinja/compare/v1.0.0-beta.2...v1.0.0-beta.3) (2023-01-02)


### Bug Fixes

* **deps:** update dependency rich to v13 ([#11](https://github.com/mirkolenz/makejinja/issues/11)) ([86b15d7](https://github.com/mirkolenz/makejinja/commit/86b15d7325c9cc4e50f69cad6c3fd5628a242817))

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

* improve compatibility with python 3.9 ([30919e8](https://github.com/mirkolenz/makejinja/commit/30919e83e11fbc368b8d97d498dab7ae2e766671))

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

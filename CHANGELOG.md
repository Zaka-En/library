# Changelog

## [1.3.0](https://github.com/Zaka-En/library/compare/v1.2.0...v1.3.0) (2026-03-23)


### Features

* StyleQuiz form compoentent ([b167d1a](https://github.com/Zaka-En/library/commit/b167d1aae0c0567b2c8838d299f2b3b5d5c001f4))

## [1.2.0](https://github.com/Zaka-En/library/compare/v1.1.0...v1.2.0) (2026-03-20)


### Features

* change color to white blend in the Book Component ([bfc402b](https://github.com/Zaka-En/library/commit/bfc402be28ae83a393232995570fc06b984befd5))
* change new font family in the Book Component ([24f6191](https://github.com/Zaka-En/library/commit/24f6191729b2f118568366699988eead5965c46e))
* color of book place holder is changed ([9921a89](https://github.com/Zaka-En/library/commit/9921a898b520a2fd069cb30cc12639b0c755427a))
* new Book emojie in the Book Component ([e5471fb](https://github.com/Zaka-En/library/commit/e5471fb80bd0749749a26bb51d73b285192a7811))


### Bug Fixes

* adjust the size of the navigation Component ([4c621ca](https://github.com/Zaka-En/library/commit/4c621ca52658d19efbeda057252cdc1b45dc71d4))

## [1.1.0](https://github.com/Zaka-En/library/compare/v1.0.0...v1.1.0) (2026-03-19)


### Features

* light blue color for the reading status component ([44433be](https://github.com/Zaka-En/library/commit/44433be8b7446131484524ad904ea85e5bc8f45a))

## 1.0.0 (2026-03-19)


### ⚠ BREAKING CHANGES

* the session generator is now a factory instead of one shared session inthe whole application

### pef

* changed all the the queries, mutations and subscription to use AsyncSession ([3b7b3ae](https://github.com/Zaka-En/library/commit/3b7b3aeb2bc1b3109db90166033298d1b80a4463))


### Features

* add CHANGELOG.md file ([079c0fb](https://github.com/Zaka-En/library/commit/079c0fb924464c4c684c9bf2511e87e01ab4f9c0))
* Add https with letsecncrypt ([851d4c6](https://github.com/Zaka-En/library/commit/851d4c69e87e972bf969e46149375bd63bb32446))
* add the ratings anchor in the header ([9f35a42](https://github.com/Zaka-En/library/commit/9f35a42889d5e9147bc623877d48812c6b6945b8))
* added a broadcast channel to sus/pub the ratings asyncronously using strawberry.subscription ([a7a57b9](https://github.com/Zaka-En/library/commit/a7a57b94b4b9eb28052b22f4ec7791dcd39fb259))
* Added a the houdini@next library and implemented it in the home page to query the reading status. Also, removed the urql logic, it no longer needed+ ([1896484](https://github.com/Zaka-En/library/commit/18964841d486cfe51edba8081bb66223a1cc9696))
* added base class and interface to services ([a1432c9](https://github.com/Zaka-En/library/commit/a1432c96100d0665550901d64d7b00a90e7b0ee4))
* added RBAC extending from BasePermission class provieded by strawberry ([250322d](https://github.com/Zaka-En/library/commit/250322deabc68594713259bab6c05bcebbb15903))
* added user model and migration ([69b5bc2](https://github.com/Zaka-En/library/commit/69b5bc2ba8ef529029f1c8230c899b1eaa6d58d5))
* algun cambio que no me acuerdo ([ecd5333](https://github.com/Zaka-En/library/commit/ecd5333ad24977ecd5ce76f58f64a35d1d0337f8))
* all the authors functionalities migrated to houdini ([102bbc3](https://github.com/Zaka-En/library/commit/102bbc3aeed4820e4bd7e641962fc4cfa5a3b17e))
* Añadir un nuevo autor, o editar la info de uno existente ([9271783](https://github.com/Zaka-En/library/commit/927178300a71998f0f381c172f6161a9237186bf))
* authentication with access and refresh token implemented with these core SvelteKit & houdini arq: ([f162235](https://github.com/Zaka-En/library/commit/f16223578ddb6dd81385cdfb8c545197b4264d01))
* Authentication with JWT using access and refresh tokens ([6aab797](https://github.com/Zaka-En/library/commit/6aab7974f1f0eb7083849e25c54369239478aaab))
* Book Crud is implemented with houdini ([4bde1df](https://github.com/Zaka-En/library/commit/4bde1dfbdfbe96554288438e1fd8e6f94650fa84))
* Calender Component ([eef583b](https://github.com/Zaka-En/library/commit/eef583b7a08d05645c2dc7bbd299c86c5889ffbd))
* calender component should work without js in the browser ([14b298c](https://github.com/Zaka-En/library/commit/14b298c597582152ddb5f1c8ce745e9eeb978d78))
* Chat open for each book component ([834920a](https://github.com/Zaka-En/library/commit/834920a58f8ca636cebf4f97574b7f0a1ba89e8e))
* Client, quieries and mutations definitions for later quering the API ([0ca3c4d](https://github.com/Zaka-En/library/commit/0ca3c4d7d564c9bc25ffdcfbc67292509cf612f4))
* conf rooms to schedule and book ([109fd14](https://github.com/Zaka-En/library/commit/109fd14cfb124a38dd0cf3ac1ab8a03239990bfe))
* conf-room is completed ([f026f41](https://github.com/Zaka-En/library/commit/f026f41126d87a8ce8f4e619fbdf5104b9486cf3))
* Implemented with houdini mutations ReadingModal to update/finish reading a book ([1e1140a](https://github.com/Zaka-En/library/commit/1e1140ab6de8be7127a52fc0e83f382bc32b415c))
* Initial implementation of relay sucessfull. Yaaaay!!! ([027ab66](https://github.com/Zaka-En/library/commit/027ab661d38fe3ab9582b2ffc1439ef00844867f))
* Initial implementation of relay sucessfull. Yaaaay!!! ([1c4799a](https://github.com/Zaka-En/library/commit/1c4799ac8ac876d78b3f5b011371f534329ad063))
* initial intent to work with auth ([6b419d5](https://github.com/Zaka-En/library/commit/6b419d539b52b7cf3e2dee820919059a48158e18))
* integrate authorization with history ([10394fd](https://github.com/Zaka-En/library/commit/10394fd27830b33717de603b1cd21c4269e8762f))
* integrate comp-library with history ([1ff0910](https://github.com/Zaka-En/library/commit/1ff09102ddf57b2b8a50dc19b92757f015d56104))
* integrate fast-graphql with commit history ([305e3db](https://github.com/Zaka-En/library/commit/305e3dba8e8038e098efe20896f9ac6d34434881))
* integrate svelte-graphql with commit history ([b4ad195](https://github.com/Zaka-En/library/commit/b4ad1955f985e52582adfca351180e522341e8ce))
* integrated auth_server with app ([1a09089](https://github.com/Zaka-En/library/commit/1a0908959a9e1b66334308159c6fb418f466df6b))
* intial intent of refactoring the fetch plugin in houdini client ([92c3b76](https://github.com/Zaka-En/library/commit/92c3b76d2859834e81aa1a9e75b02f6a75a18d6c))
* intial intent to authenticate with hooks.server.ts ([399131c](https://github.com/Zaka-En/library/commit/399131c167f1468b965f50a3ba00ab638ea3843f))
* login with jwt ([f05118d](https://github.com/Zaka-En/library/commit/f05118d90b9f5b866eead1e2a64e8e9858b0bb2f))
* models and migrations prepered for new room conference booking feature ([bf2a2de](https://github.com/Zaka-En/library/commit/bf2a2deadef184298e7a00b890b9258cc61f5687))
* My Reading status on the home page with hardcoded user ([270786a](https://github.com/Zaka-En/library/commit/270786a78f3adde414941a8245dbcc7ff4f863d1))
* new rest endpoint /refresh that refreshes the access token ([d4bb05b](https://github.com/Zaka-En/library/commit/d4bb05b39797dcbf2cd82ca63b9e39b80837b07f))
* new route /books/[id]/chat added for real time chatting about a specific book ([fe7d3ec](https://github.com/Zaka-En/library/commit/fe7d3ec61826a1d1ee0fcb21f011f722ffdaeb83))
* Pagination of authors query completedusing a customized version of the Relay standart ([92e47b7](https://github.com/Zaka-En/library/commit/92e47b79128b6e7a0bf041238c960750e8f58314))
* Pagination of the authors page complete. Added the PaginationNav componenent to seperate the logic and later reuse it ([6ab932a](https://github.com/Zaka-En/library/commit/6ab932a0bdf2de921ca2985435bb6f32ee5f5cc6))
* param id validation for authors route ([6619a28](https://github.com/Zaka-En/library/commit/6619a28d695cbb2fb32cabba65dd839ff044bdf9))
* quering conference rooms and available hours is now implemented ([ec2c4e1](https://github.com/Zaka-En/library/commit/ec2c4e13b0a2771663b264acf364cdfe9c8a8b94))
* Rate limiting logic implemented, englobed in a strawberr.permissions.BasePermission Class ([cd60f28](https://github.com/Zaka-En/library/commit/cd60f282841cc0fbee66e48f33c19b21f749488a))
* real-time chatting about a book implemented with socket subscription, mutation and pub/sus ([ea27854](https://github.com/Zaka-En/library/commit/ea27854ae09f5258268de3aeba1fcb71c69fd4c9))
* realtime notification messages to info m the client the actions within the update_author mutation ([ca5a48e](https://github.com/Zaka-En/library/commit/ca5a48e3d64c16badfe308004249a5b6923320ee))
* realtime notifications about the state of the updating an author ([a87984a](https://github.com/Zaka-En/library/commit/a87984a0c6e385a1ecb57a2683e4e8483b80bef7))
* register user added: ([9fa476a](https://github.com/Zaka-En/library/commit/9fa476a58bd92084aa0427a221fd43b49820eafe))
* simple implementation of websockets with strawberry.subscription to yield ratings with AsyncGenerator ([824ecfc](https://github.com/Zaka-En/library/commit/824ecfc5febe87c6553800f42db5c56adfffe655))
* tenia mucha prisa y me marché ([32fdd03](https://github.com/Zaka-En/library/commit/32fdd0307077b6a515ee0a1e7c3443c8a3b2dd17))
* tenia mucha prisa y me marché ([84440a5](https://github.com/Zaka-En/library/commit/84440a5dd87b46b1adf32e134290d09becba5aea))
* the reservation are now by specific hours not ranges ([bdc5173](https://github.com/Zaka-En/library/commit/bdc51734f96274d19e21fdb336f40cc25c9a464e))
* update the broadcaster to use a redis database instead of memory allowing muliprocessing to have centralized broadcast channel to pub/sub ([322acab](https://github.com/Zaka-En/library/commit/322acabece1446a3caa98ba72c9e95c1de7909dc))


### Bug Fixes

* add the .env to the git ignore, a horrible mistake ([12a8d00](https://github.com/Zaka-En/library/commit/12a8d007e94e23576cd80efd808613551929b7db))
* all problems related to builiding are fixed ([cc32bbf](https://github.com/Zaka-En/library/commit/cc32bbf814e9ce0cb04c1e49e757cfe47d53e261))
* all the ts typing problem are solvled except the jsonwebtoken package ([4134d0c](https://github.com/Zaka-En/library/commit/4134d0cd905008dabaaf9fbf561496900bdb9861))
* change finish_reading mutation to async ([ce1a2ad](https://github.com/Zaka-En/library/commit/ce1a2adfd29a0ac9403a7f365039f8e9cf0a6bf9))
* Changed to type of biobraphy from str to Optional[str] inorder to be an optional field to query and/or mutate ([5364ebf](https://github.com/Zaka-En/library/commit/5364ebf08f7656f1b6a6ecabe7f762c4536014ba))
* correcciones importantes en la lógica de las queries y las mutaciones ([34893c0](https://github.com/Zaka-En/library/commit/34893c04dd0b56c734e7471af5ce0ce01656630e))
* Dockerfile and added .dockerignore ([35d7fea](https://github.com/Zaka-En/library/commit/35d7fead4bed68310022edfb3fa6a8bf69ac0647))
* fix pnpm Dockerfile ([470736f](https://github.com/Zaka-En/library/commit/470736f02a6aa4d68f603228efb72bc77ba9efd1))
* fix some errors ([e94a511](https://github.com/Zaka-En/library/commit/e94a5114f4a06cb427d7a23d70f7ef340f8ac83a))
* fix workflow ([36bfbff](https://github.com/Zaka-En/library/commit/36bfbff5575dd509cd3546291677a1ea0d4f8eb3))
* fixed room-conf ([56bd895](https://github.com/Zaka-En/library/commit/56bd8959eec45108ef773bd4b18314b92e4d2f43))
* fixed some problem related to getting available slots in romm_booking_service ([7347cd5](https://github.com/Zaka-En/library/commit/7347cd5832216e23afc3b809107d8e7cee80c58a))
* fixed some typo problems ([b958f2c](https://github.com/Zaka-En/library/commit/b958f2c2899f641c9819a704fa416c45be1550e3))
* fixing a bunch of problems ([a7c6a24](https://github.com/Zaka-En/library/commit/a7c6a24363f2044ca658752e017d7977dfe133e5))
* fixing a bunch of problems ([7f1cd3a](https://github.com/Zaka-En/library/commit/7f1cd3a60b901f379fe98c709af65aff526c9969))
* fixing merging conflict ([295db70](https://github.com/Zaka-En/library/commit/295db7066a7803b8cf1ddae73f6a6e3dbd89339b))
* fixing typeing with typescript ([9ccc95d](https://github.com/Zaka-En/library/commit/9ccc95d2567689ab8c8957184efddb30c538bc63))
* layout.ts in books instead of page.server.ts ([c9b9dbb](https://github.com/Zaka-En/library/commit/c9b9dbbaefbd853faf7b2f6221435c4f99ec8da6))
* minor changes ([0053414](https://github.com/Zaka-En/library/commit/0053414aa6213587b93cc56e44880767b813a189))
* moved ./svelte-grpqhl/fast-grapqhl/src to ./svelte-grpqhl ([43c22b6](https://github.com/Zaka-En/library/commit/43c22b607ba25030176912e5b14d009e9671f128))
* remove all the code inside the __init__ files to solve circular deps problems ([cbc77e2](https://github.com/Zaka-En/library/commit/cbc77e2959fa57fe51c65ab0e95c4ea32d4b500b))
* remove the version spec fron the test.yml ([02e6528](https://github.com/Zaka-En/library/commit/02e6528b8160b255e4d8e4ac3b5dd52fa71b4d7c))
* removed unnecesay directory Diseño final ([3182b47](https://github.com/Zaka-En/library/commit/3182b47688dbbae3a20cac00403a75e23aabd17a))
* set config auth workflow to use a repository secret ([2f5f7cb](https://github.com/Zaka-En/library/commit/2f5f7cb9ac86f2e4ada8c01090e79ffba41cbd0a))
* Stop tracking .env ([b283f2b](https://github.com/Zaka-En/library/commit/b283f2b4af794e623f175801137b153e4dfb6fe9))
* this a special commit I did before cherry-picking ([1961145](https://github.com/Zaka-En/library/commit/1961145c53b7817d160eedf22ec27e594f43e7f0))
* typing issues in typescript ([1f0da8d](https://github.com/Zaka-En/library/commit/1f0da8ddde64b64ec709d09c5d2c35aa721299a2))
* update Book comp ([0329b3d](https://github.com/Zaka-En/library/commit/0329b3dfca9d5de8143c9f988d795eba26ea037d))
* update the +page.svelte of the root to use render children instead of slot ([f768f55](https://github.com/Zaka-En/library/commit/f768f55a7481342bfeab7bcd4caf2289c69d6eb4))
* use correct message for http exceptions ([e756b37](https://github.com/Zaka-En/library/commit/e756b372c6cdd255e73399ee91ca91a2d070cd8d))
* use the right order of exceptions + ([3c861d3](https://github.com/Zaka-En/library/commit/3c861d380c2f5070ed77f6696df7cd9103a5fc3c))
* username of model user to nullable ([d99c3c9](https://github.com/Zaka-En/library/commit/d99c3c9384eeed4edc13d10aab38e7caf67fe7f3))

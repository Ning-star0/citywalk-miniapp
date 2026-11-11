# GitHub协作规则

## 首次加入

成员使用自己的GitHub账号。加入仓库后：
```sh
git clone <实际仓库URL>
cd guiyang-citywalk
git switch -c feat/member4-route-filters
npm run check
```

主分支使用main，不增加一条长期dev分支。每项Issue对应一个短期分支：
feat/memberN-topic、fix/memberN-topic、data/member2-topic、docs/memberN-topic。

## 提交与合并

1. 从最新main建分支，在Issue中声明认领。
2. 只修改自己任务涉及的目录；跨模块变更先协商。
3. 修改XML后执行npm run data:build并一起提交生成物。
4. 运行npm run check；页面变更附微信开发者工具截图及测试步骤。
5. 提交Pull Request，正文写Closes #实际Issue号，说明交付与未完成项。
6. 成员1审阅并合并，数据相关PR同时由成员3复核。
7. 普通成员不直接push main；保护规则需负责人在GitHub实际启用，模板本身不会自动保护分支。

## 敏感信息

不提交AppSecret、密钥、令牌、.env、服务器密码或project.private.config.json。
project.config.json保留touristappid。各成员在本机开发者工具中选择自己的AppID。
不要把本机绝对路径、其他课程资料或服务器配置中无关的秘密上传到仓库。

## 推荐仓库设置

建议私有仓库；开启Issues；为main要求PR和CI检查（套餐不支持时执行人工审阅）。
CODEOWNERS目前仅登记架构负责人；成员账号齐全后再添加目录负责人。
GitHub Project看板可使用Todo、In progress、Review、Done四列；尚未自动创建。

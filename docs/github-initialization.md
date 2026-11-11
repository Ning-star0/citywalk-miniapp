# GitHub初始化状态

本地仓库已包含main分支、源码、Issue/PR模板、CODEOWNERS、CI和12项待认领任务。
目标账号：Ning-star0；建议仓库名：guiyang-citywalk；建议可见性：Private。

当前GitHub连接器支持提交文件、创建Issue等操作，但未提供创建仓库接口。
浏览器创建仓库入口已打开，尚需用户登录；在远程实际创建成功前不应把计划URL当成已存在仓库。

下一步由负责人登录GitHub并新建空仓库，或告知已建仓库的URL。
不要勾选自动生成README、.gitignore或许可证，本地已有这些项目文件（本项目尚未选许可证）。
创建后可用连接器提交内容并创建12个Issue，或在已认证的Git环境执行：

```sh
git remote add origin https://github.com/Ning-star0/guiyang-citywalk.git
git push -u origin main
```

任务清单为.github/tasks.json；如果已安装并登录GitHub CLI，可执行：

```sh
python3 scripts/publish_issues.py --repo Ning-star0/guiyang-citywalk --dry-run
python3 scripts/publish_issues.py --repo Ning-star0/guiyang-citywalk
```

不要在仓库、Issue或聊天中粘贴GitHub访问令牌。成员账号未确定前只按编号认领，不自动添加外部协作者。

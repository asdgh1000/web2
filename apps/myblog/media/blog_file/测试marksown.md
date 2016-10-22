网上找了一下，用Octopress 加GitHup Pages 搭建自己的博客比较简单和高效，所以花了一下午，折腾了一番，算是搭建
好自己的博客网站了吧，之后再慢慢优化。第一个博客，就记录下整个搭建过程吧，因为我只搭建了Octopress的基本的东西，
整个过程比较简单，这里只记录一下简单的步骤，以后会不断的加入完善这个博客的过程。

###  Octopress 安装

&emsp;&emsp;Octopress 安装过程安照[官网](http://octopress.org/docs/setup)的步骤一步步走下来，遇到的问题是ruby的源默
认识官网的，在国内因为一些你懂得原因会导致一些依赖安装不了。需要换一个国内的源，找了下资料，
改成[淘宝的源](https://ruby.taobao.org)就可以了（淘宝这点不错，很多东西他都有开放的源）。具体方法：

* 添加淘宝的源：
```bash
gem sources -a http://ruby.taobao.org
```
* 删除官方的源，确保只有淘宝的源：
```bash
gem sources -r https://rubygems.org
```
* 查看源列表：
```bash
gem sources
```
&emsp;&emsp;完成了上面的步骤后，发现一些依赖是可以安装了，但是还是有依赖不能安装，看终端提示，发现程序还是到官网的源去下载
依赖包了，之前没有使用过ruby，不知道什么原因，网上查了一些资料没找到结果。换个思路，去了解了下ruby，发现ruby项目
的依赖关系是在Gemfile文件中定义了。果然，octopress 目录下有这个文件，把里面的source改成淘宝的源，一切就OK了。

### 关联到GitHup Pages

&emsp;&emsp; 部署Octopress 的方式有好多种，官网上提供了三种方式的教程，参考这个页面[http://octopress.org/docs/deploying](http://octopress.org/docs/deploying/)。
我这里使用的自然是[GitHup Pages](http://octopress.org/docs/deploying/github/)，参考这个链接的教程，很容易的就把
GitHup Pages 部署好了，这里可能需要注意的地方是在github上新建项目的时候注意不要选自动生成README.md的那个选项，
我一开始手贱点了，发现在使用`rake deploy` 命令时一直提示本地内容落后远程的，pull远程内容也不行，最后把项目删了重建
后才解决的问题。

&emsp;&emsp;我这里暂时没有关联自定义的域名（因为没有啊。。。反正现在自己看，以后如果有读者的话我再加上吧）。

### 修改首页的基本信息

&emsp;&emsp;完成上面的所有步骤，就可以打开[博客首页](http://hello-wood.github.io)，当然一开始的首页只有一个Octopress的默认界面
，需要修改一些配置信息。在_config.yml中修改博客的主标题和自己的名字以及邮箱信息。

### 完成第一篇博客

&emsp;&emsp;最后，开始我的第一篇博客，也就是本文的内容了，在Octopress目录下输入：
```bash
rake new_post
```
会提示输入title，输入你想输入的标题后，会在source/_posts 目录下生成日期+标题的markdown文件，用你擅长的
编辑器打开，就可以按照markdown 的语法编写自己的博客了。编写完博客后，输入指令：
```bash
rake gen_deploy
```
大功告成，刷你的GitHup Pages页面，就可以看到你写的博客了！

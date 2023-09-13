# Depressive Disorder Detection System

### 系统结构

前端Vue3 + Vite + Vue Router，后端服务器Flask（记得先启服务器再开前端）

---

### 前端

#### 前端配置
1. 屏幕设置：在Chrome浏览器的开发者工具里，点开"元素"左边那个图标，在尺寸里添加自定义设备，宽1200x长1920，像素比0.1125
>一定不要忘了按照上边这个步骤配置屏幕设置以实现等比预览，建议使用Chrome浏览器

2. pull本项目之后首先进入/detection-front-end目录下，输入命令行
`npm install`安装全部依赖
3. 输入命令行 `npm run dev` 在Chrome浏览器打开（使用设置好的屏幕尺寸预览）

---

#### 前端路由
>可以通过在地址后边加路径直接跳转具体单一页面
1. 着陆页 /
2. 量表填写页 /1
3. 情绪图片观看页 /2
4. 结果显示页 /result


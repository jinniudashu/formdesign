## 服务设计子系统 | [English](../README.md)

### 🚀 特性
#### 本项目是健康管理应用定制系统组成部分——服务设计子系统

* 健康管理应用的目标是协同，把正确的信息在正确的时间点推送到正确的人面前。

* 解决这一问题的根本方法，是为每个参与协作的人员生成一个合适的下一个任务，“合适”的意思是符合预设的业务规则。

* 为满足医疗保健行业的独特需求，需要由业务设计人员定制服务任务和业务规则，系统把业务设计马上生成业务应用发布运行。

* 这个由业务设计人员定制的应用可以根据预设的业务规则协同多位健康照护专家的服务任务，完成用户服务任务。

* HSSC运行时框架子系统导入设计子系统生成的业务系统脚本，migration后，即可发布运行，整个过程可以在10分钟内完成。

* 服务任务会按照业务管理人员定义的业务规则在正确的时间点被推送到每位健康照护专家的工作台上的任务清单里，以实现高效的团队协作。

* 参考运行时框架子系统：https://github.com/jinniudashu/hssc

### 🧠 核心概念
核心业务模型由七个关键元素构成，这是一个通用的协作系统抽象：
1. 服务任务：用服务任务的元信息，管理属性，业务属性来定义。
2. 服务表单：服务任务的工作成果，由多个业务字段的键值对组成的JSON表单来表示。
3. 业务事件：当服务表单中的业务字段值满足某种条件时（对应一个逻辑表达式），认为发生了某种业务事件。
4. 服务规则：完成服务任务后，如果发生某个业务事件时，应该采取什么行动（系统作业）。
5. 系统作业：系统调度动作，用于维护服务进程状态或发送消息。目前有四个调度动作：生成下一个任务；推荐下一个任务；发送微信公众号消息；发送企业微信消息。
6. 服务进程：服务任务运行时，用于管理调度服务任务状态。
7. 调度器：在服务进程状态变化时，根据业务规则判断要做出哪个系统调度动作。

![核心业务模型关系图](./7elements.png)

### 安装使用
#### 📋 Requirements
* .env file is required at the root directory of the project, please refer to .env.example for the required environment variables.

* If there are computed fields in the designing, OPENAI_API_KEY is required to generating JS code.

#### 🛠️ Manual Installation
1. Clone the code repository to your local machine:
```bash
    git clone https://github.com/your_username/formdesign.git
```
2. Navigate to the project directory:
```bash
    cd formdesign
```
3. Create a virtual environment:
```bash
    python -m venv env
    source env/bin/activate  # Linux or macOS
    .\env\Scripts\activate  # Windows
```
4. Install the dependencies:
```bash
    pip install -r requirements.txt
```
5. Perform database migration:
```bash
    python manage.py migrate
```
6. Create a superuser account:
```bash
    python manage.py createsuperuser
```
8. Load the dictionary and design data:
```bash
    python manage.py restore_icpc
    python manage.py restore_design
```
9. Run the development server on port 8001 if you are running the HSSC application on port 8000:
```bash
    python manage.py runserver 8001
```
10. Open http://127.0.0.1:8001/admin in your browser to check if the application has started correctly.

Congratulations! You have successfully installed and run the Formdesign subsystem.

#### 🔧 Usage
1. 设计系统定义服务任务、服务表单、业务事件、业务规则、服务角色，用这些部件组成项目，生成应用系统脚本。
![构成项目的要素](./project-elements.png)
* 定义字典
* 定义字段
* 定义服务表单：表单是字段的集合
* 定义服务任务：服务任务是服务元数据和表单的集合
* 定义服务包：编排具有特定时间关系的多个服务任务
* 定义业务事件：业务事件是表单字段的逻辑表达式
* 定义服务规则：定义业务事件发生时的系统作业
* 定义管理实体：服务任务面向管理实体，每个服务任务都是对特定管理实体属性信息的加工
* 定义服务角色：服务角色有特定服务任务的操作权限
* 定义项目：项目是服务任务、服务包、、服务规则、服务角色的集合
* 生成应用系统脚本
* 生成设计数据备份
* 备份设计数据到本地文件
* 恢复设计数据

2. Backup design to local file:
```bash
    python manage.py backup_design_tolocal
```
3. Restore design from local file:
```bash
    python manage.py restore_design
```
4. Backup dictionary to local file:
```bash
    python manage.py backup_icpc_tolocal
```
5. Restore dictionary from local file:
```bash
    python manage.py restore_icpc
```
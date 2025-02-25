const task = {
  "task.list.title": { cn: "任务列表", en: "Task List", },
  "task.list.actions.detail": { cn: "详情", en: "Detail", },
  "task.detail.title": { cn: "任务详情", en: "Task Detail", },
  "task.asset.title": { cn: "数据详情", en: "Task Assets", },
  "task.all": { cn: "全部", en: "All", },
  "task.type.train": { cn: "训练任务", en: "Train", },
  "task.type.mine": { cn: "挖掘任务", en: "Mining", },
  "task.type.label": { cn: "标注任务", en: "Label", },
  "task.type.filter": { cn: "筛选任务", en: "Filter", },
  "task.type.import": { cn: "导入任务", en: "Import", },
  "task.state.pending": { cn: "排队中", en: "Queuing", },
  "task.state.doing": { cn: "进行中", en: "In-Progress", },
  "task.state.finish": { cn: "完成", en: "Finish", },
  "task.state.failure": { cn: "失败", en: "Failure", },
  "task.column.name": { cn: "任务名称", en: "Task Name", },
  "task.column.type": { cn: "任务类型", en: "Type", },
  "task.column.state": { cn: "任务进度", en: "Progress", },
  "task.column.state.timeleft.label": { cn: "剩余时间：", en: "Time Left: ", },
  "task.column.create_time": { cn: "创建时间", en: "Create Time", },
  "task.column.action": { cn: "操作", en: "Actions", },
  "task.add.option.filter": { cn: "筛选任务", en: "Filter", },
  "task.add.option.train": { cn: "训练任务", en: "Train", },
  "task.add.option.mine": { cn: "挖掘任务", en: "Mining", },
  "task.add.option.label": { cn: "标注任务", en: "Label", },
  "task.action.filter": { cn: "筛选", en: "Filter", },
  "task.action.train": { cn: "训练", en: "Train", },
  "task.action.mine": { cn: "挖掘", en: "Mining", },
  "task.action.label": { cn: "标注", en: "Label", },
  "task.action.edit": { cn: "编辑", en: "Rename", },
  "task.action.del": { cn: "删除", en: "Remove", },
  "task.action.stop": { cn: "终止", en: "Terminate", },
  "task.action.copy": { cn: "复制", en: "Copy", },
  "task.action.labelplatform": { cn: "标注平台", en: "Label Platform", },
  "task.action.labeldata": { cn: "获取标注数据", en: "Label Data", },
  "task.action.history": { cn: "历史树", en: "History", },
  "task.action.detail": { cn: "详情", en: "Detail", },
  "task.empty.label": { cn: "新建一个任务", en: "Create a task", },
  "task.add.label": { cn: "新建", en: "Create", },
  "task.query.name": { cn: "任务名称", en: "Task Name", },
  "task.query.type": { cn: "类型", en: "Type", },
  "task.query.createtime": { cn: "创建时间", en: "Create Time", },
  "task.times.current": { cn: "当天", en: "Today", },
  "task.times.3day": { cn: "近三天", en: "Last 3 Days", },
  "task.times.week": { cn: "近一周", en: "Last Week", },
  "task.times.year": { cn: "近一年", en: "Last Year", },
  "task.query": { cn: "查询", en: "Search", },
  "task.reset": { cn: "重置", en: "Reset", },
  "task.action.multi.train": { cn: "批量训练", en: "Train With", },
  "task.action.multi.mine": { cn: "批量挖掘", en: "Mining With", },
  "task.cancel.select": { cn: "取消选择", en: "Cancel Select", },
  "task.action.del.confirm.content": { cn: "确认要删除任务：{name}？", en: "Are you sure to remove this task: {name}?", },
  "task.action.stop.confirm.content": { cn: "确认要终止任务：{name}？", en: "Are you sure to terminate the task: {name}?", },
  "task.action.getlabels.confirm.content": { cn: "确认要获取当前标注数据并终止任务：{name}？", en: "Are you sure to get current labelled data and terminate this task:{name}?", },
  "task.query.name.placeholder": { cn: "任务名称", en: "Task Name", },
  "task.selected.label": { cn: "已选择 {len} 项, ", en: "{len} tasks selected, ", },
  "task.pager.total.label": { cn: "共 {total} 项", en: "Total {total} items", },
  "task.detail.label.name": { cn: "任务名称", en: "Task Name", },
  "task.detail.label.id": { cn: "任务ID", en: "Task ID", },
  "task.detail.label.map": { cn: "mAP值", en: "mAP", },
  "task.detail.label.source": { cn: "任务来源", en: "Source", },
  "task.detail.label.training_dataset": { cn: "训练集", en: "Training Dataset", },
  "task.detail.label.verify_dataset": { cn: "验证集", en: "Verify Dataset", },
  "task.detail.label.test_dataset": { cn: "测试集", en: "Test Dataset", },
  "task.detail.label.dataset_percent": { cn: "训练/验证/测试集比例", en: "Train / Verify / Test", },
  "task.detail.label.train_type": { cn: "训练类型", en: "Train Type", },
  "task.detail.label.train_goal": { cn: "训练目标", en: "Train Classes", },
  "task.detail.label.framework": { cn: "算法框架", en: "Network", },
  "task.detail.label.create_time": { cn: "创建时间", en: "Created", },
  "task.detail.label.backbone": { cn: "骨干网络结构", en: "Backbone", },
  "task.detail.label.hyperparams": { cn: "超参数", en: "Hyper Parameters", },
  "task.detail.state.title": { cn: "任务状态", en: "Task State", },
  "task.detail.state.current": { cn: "当前状态", en: "Current State", },
  "task.detail.result.title": { cn: "任务结果", en: "Task Result", },
  "task.detail.dataset.name": { cn: "数据集名称", en: "Dataset Name", },
  "task.detail.error.code": { cn: "失败原因", en: "Error Reason", },
  "task.detail.error.desc": { cn: "失败描述", en: "Error Desc", },
  "task.detail.label.download.btn": { cn: "下载标注描述文档", en: "Download Label Desc Doc", },
  "task.detail.error.title": { cn: "失败", en: "Failure", },
  "task.filter.create.success.msg": { cn: "创建成功", en: "Create Task Success!", },
  "task.filter.form.name.label": { cn: "任务名称", en: "Task Name", },
  "task.filter.form.name.placeholder": { cn: "请输入任务名称", en: "Task Name, example \"task_0001\"", },
  "task.filter.form.name.required": { cn: "请输入任务名称", en: "Please enter your task name", },
  "task.filter.form.datasets.label": { cn: "数据集", en: "Datasets", },
  "task.filter.form.datasets.required": { cn: "数据集不能为空，请选择数据集", en: "Datasets is required, please select dataset more than one", },
  "task.filter.form.datasets.placeholder": { cn: "请选择数据集", en: "Select/Filter Datasets", },
  "task.filter.form.include.label": { cn: "筛选标签", en: "Keywords", },
  "task.filter.form.include.required": { cn: "请选择筛选标签", en: "Please select keywords for filter", },
  "task.filter.form.exclude.label": { cn: "排除标签", en: "Exclude Keywords", },
  "task.train.form.valastest": { cn: "使用验证集作为测试集", en: "Use Validation Sets as Test Sets", },
  "task.train.form.trainsets.label": { cn: "训练集", en: "Train Sets", },
  "task.train.form.testsets.label": { cn: "测试集", en: "Test Sets", },
  "task.train.form.keywords.label": { cn: "训练目标", en: "Train Classes", },
  "task.train.keywords.placeholder": { cn: "训练目标是训练集的标签和数据集的标签的交集", en: "Train Classes is both in train sets and test sets", },
  "task.train.form.keywords.required": { cn: "请选择训练目标", en: "Please select your train classes", },
  "task.train.form.traintype.label": { cn: "训练类型", en: "Train Type", },
  "task.train.form.network.label": { cn: "算法框架", en: "Network", },
  "task.train.form.backbone.label": { cn: "骨干网络结构", en: "Backbone", },
  "task.train.form.hyperparam.label": { cn: "超参数", en: "Hyper Params", },
  "task.train.form.traintypes.detect": { cn: "目标检测", en: "Object Detection", },
  "task.train.total.label": { cn: "共 {total} 个", en: "Total {total} assets", },
  "task.train.form.repeatdata.label": { cn: "当数据重复时：", en: "Found duplicate data: ", },
  "task.train.form.repeatdata.terminate": { cn: "终止任务", en: "Terminate Task", },
  "task.train.form.repeatdata.latest": { cn: "采用最新的标注", en: "Use Data With Latest Annotation", },
  "task.train.form.repeatdata.original": { cn: "采用最初的标注", en: "Use Data With Original Annotation", },
  "task.filter.create": { cn: "创建任务", en: "Create Task", },
  "task.mining.form.excludeset.label": { cn: "排除数据集", en: "Exclude Datasets", },
  "task.mining.form.model.label": { cn: "模型", en: "Model", },
  "task.mining.form.model.required": { cn: "请选择模型", en: "Plese select a model", },
  "task.mining.form.algo.label": { cn: "挖掘算法", en: "Mining Algorithm", },
  "task.mining.form.strategy.label": { cn: "筛选策略", en: "Filter Strategy", },
  "task.mining.form.topk.label": { cn: "TOPK", en: "TOP K", },
  "task.label.form.type.newer": { cn: "未标注部分", en: "Unlabel", },
  "task.mining.form.label.label": { cn: "是否产生新标注", en: "With Annotations", },
  "task.mining.form.label.no": { cn: "否", en: "No", },
  "task.mining.form.label.yes": { cn: "是", en: "Yes", },
  "task.mining.topk.tip": { cn: "TOPK值大于选中数据集大小时，返回全部数据", en: "Top k large than total data will return all data", },
  "task.validator.same.param": { cn: "参数key重复", en: "Duplicate key of params", },
  "task.label.form.type.all": { cn: "全部重新标注", en: "All", },
  "task.label.form.member": { cn: "标注人员", en: "Labeller", },
  "task.label.form.member.required": { cn: "请输入标注人员的邮箱", en: "Please enter labeller's email", },
  "task.label.form.member.placeholder": { cn: "请输入标注人员的邮箱", en: "Please input labeller's email", },
  "task.label.form.member.email.msg": { cn: "请输入正确的邮箱格式", en: "Please input valid EMAIL", },
  "task.label.form.target.label": { cn: "标注目标", en: "Label Classes", },
  "task.label.form.target.placeholder": { cn: "请选择标注目标", en: "Please select label classes", },
  "task.label.form.desc.label": { cn: "标注描述文件", en: "Desc File", },
  "task.label.form.desc.info": { cn: "1. 允许上传doc、docx、pdf等文档{br} 2. 文件大小不超过50M", en: "1. *.doc, *.docx, *.pdf allowed {br} 2. file size < 50M", },
  "task.label.form.plat.checker": { cn: "到标注平台查看", en: "View In Label Platform", },
  "task.label.form.plat.label": { cn: "标注平台账号", en: "Label Platform Account", },
  "task.label.form.plat.go": { cn: "到标注平台注册账号", en: "Label Platform", },
  "task.label.form.label.label": { cn: "是否带原标注", en: "With Original Annotations", },
  "task.filter.tip.keyword.required": { cn: "筛选标签和排除标签至少需要选择1个", en: "There should be more than 1 selected on filter keywords and exclude filter keywords", },
  "task.train.fold": { cn: '收起参数配置', en: 'Fold', },
  "task.train.unfold": { cn: '展开参数配置', en: 'Unfold', },
  "task.train.parameter.add.label": { cn: '添加自定义参数', en: 'Add Custom Parameter', },
  "task.label.bottomtip": { cn: '没有标注人员账号or邮箱，我要{link}', en: 'None of labeller account, {link}', },
  "task.label.bottomtip.link.label": { cn: '注册标注平台账号>>', en: 'sign up Label Platform Account >>', },
  "task.btn.back": { cn: '返回', en: 'BACK', },
  "task.gpu.count": { cn: 'GPU个数', en: 'GPU Count', },
  "task.detail.model.deleted": { cn: '已删除', en: 'Deleted', },
  'task.detail.label.go.platform': { cn: '跳转到标注平台>>', en: 'Go to Label Platform >>' },
}

export default task

const dataset = {
  "dataset.list.title": { cn: "数据集列表", en: "Dataset List", },
  "dataset.list.actions.detail": { cn: "详情", en: "Detail", },
  "dataset.detail.title": { cn: "数据集详情", en: "Dataset Detail", },
  "dataset.asset.title": { cn: "数据详情", en: "Dataset Assets", },
  "dataset.all": { cn: "全部", en: "All", },
  "dataset.type.train": { cn: "训练任务", en: "Train Task", },
  "dataset.type.mine": { cn: "挖掘任务", en: "Mining Task", },
  "dataset.type.label": { cn: "标注任务", en: "Label Task", },
  "dataset.type.filter": { cn: "筛选任务", en: "Filter Task", },
  "dataset.type.import": { cn: "导入", en: "Import", },
  "dataset.state.importing": { cn: "正在导入", en: "Importing", },
  "dataset.state.imported": { cn: "导入成功", en: "Imported", },
  "dataset.state.failure": { cn: "导入失败", en: "Import Failure", },
  "dataset.column.name": { cn: "名称", en: "Dataset Name", },
  "dataset.column.source": { cn: "来源", en: "Source", },
  "dataset.column.asset_count": { cn: "图片数", en: "Assets' Count", },
  "dataset.column.keyword": { cn: "标签", en: "Keywords", },
  "dataset.column.ignored_keyword": { cn: "忽略标签", en: "Ignored Keywords", },
  "dataset.column.state": { cn: "状态", en: "Status", },
  "dataset.column.create_time": { cn: "创建时间", en: "Create Time", },
  "dataset.column.action": { cn: "操作", en: "Actions", },
  "dataset.column.keyword.label": { cn: "{keywords} 共{total}个", en: "{keywords} total {total}.", },
  "dataset.action.filter": { cn: "筛选", en: "Filter", },
  "dataset.action.train": { cn: "训练", en: "Train", },
  "dataset.action.mining": { cn: "挖掘", en: "Mining", },
  "dataset.action.label": { cn: "标注", en: "Label", },
  "dataset.action.del": { cn: "删除", en: "Remove", },
  "dataset.action.history": { cn: "历史树", en: "History", },
  "dataset.action.detail": { cn: "详情", en: "Detail", },
  "dataset.action.edit": { cn: "编辑", en: "Rename", },
  'dataset.action.inference': { cn: '推理', en: 'Inference', },
  "dataset.empty.label": { cn: "去导入一个数据集", en: "Import A Dataset", },
  "dataset.import.label": { cn: "导入数据集", en: "Import Dataset", },
  "dataset.query.name": { cn: "名称", en: "Dataset Name", },
  "dataset.query.source": { cn: "数据来源", en: "Source", },
  "dataset.query.createtime": { cn: "创建时间", en: "Create Time", },
  "dataset.times.current": { cn: "当天", en: "Today", },
  "dataset.times.3day": { cn: "近三天", en: "Last 3 Days", },
  "dataset.times.week": { cn: "近一周", en: "Last Week", },
  "dataset.times.year": { cn: "近一年", en: "Last Year", },
  "dataset.query": { cn: "查询", en: "Search", },
  "dataset.reset": { cn: "重置", en: "Reset", },
  "dataset.action.multi.train": { cn: "去训练", en: "Train With", },
  "dataset.action.multi.mine": { cn: "去挖掘", en: "Mining With", },
  "dataset.cancel.select": { cn: "取消选择", en: "Cancel Select", },
  "dataset.action.del.confirm.content": { cn: "确认要删除数据集：{name}？", en: "Are you sure to remove this dataset:{name}?", },
  "dataset.query.name.placeholder": { cn: "数据集名称", en: "Dataset Name", },
  "dataset.selected.label": { cn: "已选择 {len} 项，共计图片 {count} 张，", en: "{len} datasets selected，total {count} assets.", },
  "dataset.pager.total.label": { cn: "共 {total} 项", en: "Total {total} items", },
  "dataset.detail.pager.total": { cn: "总共包含 {total} 图像", en: "Total {total} pictures", },
  "dataset.detail.keyword.label": { cn: "标签：", en: "Keywords: ", },
  "dataset.detail.randompage.label": { cn: "随机页", en: "Random Page", },
  "dataset.detail.assets.keywords.total": { cn: "共{total}个标签", en: "{total} keywords", },
  "dataset.asset.info": { cn: "数据信息", en: "Asset Info", },
  "dataset.asset.info.id": { cn: "标识", en: "ID", },
  "dataset.asset.info.size": { cn: "大小", en: "Size", },
  "dataset.asset.info.width": { cn: "宽", en: "Width", },
  "dataset.asset.info.height": { cn: "高", en: "Height", },
  "dataset.asset.info.channel": { cn: "通道", en: "Channels", },
  "dataset.asset.info.timestamp": { cn: "时间戳", en: "Timestamp", },
  "dataset.asset.info.keyword": { cn: "标签", en: "Keywords", },
  "dataset.asset.random": { cn: "随机图像", en: "Random Asset", },
  "dataset.asset.empty": { cn: "查询不到指定asset", en: "Invalid Asset", },
  "dataset.asset.annotation.hide": { cn: "隐藏所有标注", en: "Hide All", },
  "dataset.asset.annotation.show": { cn: "显示所有标注", en: "Show All", },
  "dataset.add.types.internal": { cn: "公共数据集", en: "Public Dataset", },
  "dataset.add.types.share": { cn: "用户分享数据集", en: "Shared Dataset", },
  "dataset.add.types.net": { cn: "网络导入", en: "Net Import", },
  "dataset.add.types.local": { cn: "本地导入", en: "Local Import", },
  "dataset.add.types.path": { cn: "路径导入", en: "Path Import", },
  "dataset.add.success.msg": { cn: "导入任务创建成功！正在导入...", en: "Import dataset task created! Importing...", },
  "dataset.add.form.name.label": { cn: "名称", en: "Name", },
  "dataset.add.form.name.required": { cn: "请输入数据集名称", en: "Dataset Name", },
  "dataset.add.form.type.label": { cn: "导入类型", en: "Type", },
  "dataset.add.form.label.label": { cn: "导入标注", en: "Type", },
  "dataset.add.form.newkw.label": { cn: " ", en: " ", },
  "dataset.add.newkw.asname": { cn: "添加标签", en: "As Keyword", },
  "dataset.add.newkw.asalias": { cn: "添加为别名", en: "As Alias", },
  "dataset.add.newkw.ignore": { cn: "忽略此标签", en: "Ignore", },
  "dataset.add.form.newkws.label": { cn: "添加标签", en: "Add Keywords", },
  "dataset.add.form.newkw.link": { cn: "去添加>>", en: "Add New Keywords>>", },
  "dataset.add.form.newkw.tip": { cn: "当导入数据集的标签不属于当前标签时，选择标签合并策略", 
  en: "Select keyword merging strategy for new keywords", },
  "dataset.add.label_strategy.include": { cn: "包含标注", en: "Include Annotations", },
  "dataset.add.label_strategy.exclude": { cn: "不包含标注", en: "Exclude Annotations", },
  "dataset.add.label_strategy.ignore": { cn: "忽略新标签和对应标注", en: "Ignore unknown keywords and annotations", },
  "dataset.add.label_strategy.add": { cn: "添加到标签列表", en: "Add Keywords to your Keywords List", },
  "dataset.add.label_strategy.stop": { cn: "终止任务", en: "Terminate Task", },
  "dataset.add.form.internal.label": { cn: "数据集", en: "Dataset", },
  "dataset.add.form.internal.required": { cn: "请选择公共数据集", en: "Please select public dataset", },
  "dataset.add.form.internal.placeholder": { cn: "请选择一个公共数据集", en: "Select A Public Dataset", },
  "dataset.add.form.share.label": { cn: "数据集ID", en: "Dataset ID", },
  "dataset.add.form.share.required": { cn: "请输入分享ID", en: "Please input share ID", },
  "dataset.add.form.share.placeholder": { cn: "请输入待分享的数据集ID", en: "Share ID", },
  "dataset.add.form.net.label": { cn: "URL地址", en: "URL", },
  "dataset.add.form.net.tip": { cn: "请输入压缩文件的url地址", en: "Please input a url of zip file", },
  "dataset.add.form.path.label": { cn: "路径", en: "Path", },
  "dataset.add.form.path.tip": { cn: "请输入数据集在服务器中的绝对路径，如 /home/users/dataset/train_cat", en: "Please input absolute path of dataset on server, like: /home/users/dataset/train_cat", },
  "dataset.add.form.path.placeholder": { cn: "请输入服务端的绝对路径", en: "Please input absolute path of dataset on server", },
  "dataset.add.form.upload.btn": { cn: "上传文件", en: "Upload", },
  "dataset.add.form.upload.tip": {
    cn: `1. 仅支持zip格式压缩包文件上传；{br}
      2. 局域网内压缩包大小 < 1G, 互联网建议 < 200MB；{br}
      3. 压缩包内图片格式要求为：图片格式为*.jpg、*.jpeg、*.png、*.bmp，标注文件格式为pascal。{br}
      4. 压缩包文件内图片文件需放入images文件夹内，标注文件需放入annotations文件夹内，如以下示例：{sample}`, 
    en: `1. Only zip file allowed;{br} 
      2. Size < 1G;{br}
      3. Images format allowed *.jpg, *.jpeg, *.png, *.bmp, annotations format supported pascal(*.xml)
      4. Sample: {sample}`
  },
  'dataset.detail.info': { cn: '详细信息', en: '', },
  'dataset.detail.action.filter': { cn: '筛选数据集', en: 'Filter Dataset', },
  'dataset.detail.action.train': { cn: '训练模型', en: 'Train Model', },
  'dataset.detail.action.mining': { cn: '挖掘数据', en: 'Mining', },
  'dataset.detail.action.label': { cn: '标注数据', en: 'Label', },
  'dataset.detail.info.keyword.label': { cn: '标签共{total}个', en: 'Total {total} Keywords:', },
  'dataset.import.public.include': { cn: '包含标签', en: 'Include', },
  'dataset.add.newkeyword.empty': { cn: '无新标签', en: 'None of new keywords', },
  'dataset.add.local.file.empty': { cn: '请上传本地文件', en: 'Please upload a zip file', },
}

export default dataset

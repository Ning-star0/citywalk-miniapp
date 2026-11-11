const repo=require('../../services/catalog');const config=require('../../config');
Page({
 data:{keyword:'',district:'全部',metroStation:'全部',maxMinutes:0,includeDrafts:config.includeDrafts,
 districts:['全部',...new Set(repo.catalog.routes.map(r=>r.district))],metros:['全部',...new Set(repo.catalog.routes.map(r=>r.metroStation))],
 durations:[{label:'全部耗时',value:0},{label:'90分钟内',value:90},{label:'120分钟内',value:120}],results:[]},
 onLoad(){this.refresh();},
 refresh(){this.setData({results:repo.list(this.data)});},
 search(e){this.setData({keyword:e.detail.value});this.refresh();},
 filter(e){const {key,value}=e.currentTarget.dataset;if(!['district','metroStation','maxMinutes'].includes(key))return;this.setData({[key]:value});this.refresh();},
 reset(){this.setData({keyword:'',district:'全部',metroStation:'全部',maxMinutes:0});this.refresh();},
 open(e){wx.navigateTo({url:'/pages/detail/detail?id='+e.currentTarget.dataset.id});}
});

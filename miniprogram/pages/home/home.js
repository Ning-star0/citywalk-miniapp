const repo=require('../../services/catalog');const config=require('../../config');
Page({
 data:{city:repo.catalog.city,version:repo.catalog.datasetVersion,routes:repo.list({includeDrafts:config.includeDrafts})},
 open(e){wx.navigateTo({url:'/pages/detail/detail?id='+e.currentTarget.dataset.id});},
 routes(){wx.switchTab({url:'/pages/routes/routes'});}
});

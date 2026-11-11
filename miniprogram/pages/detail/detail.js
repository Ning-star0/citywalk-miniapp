const repo=require('../../services/catalog');const favorites=require('../../services/favorites');
Page({
 data:{route:null,saved:false},
 onLoad(options){const route=repo.detail(options.id);if(route)this.setData({route,saved:favorites.list().includes(route.id)});},
 onShow(){if(this.data.route)this.setData({saved:favorites.list().includes(this.data.route.id)});},
 favorite(){try{this.setData({saved:favorites.toggle(this.data.route.id)});wx.showToast({title:this.data.saved?'已收藏':'已取消',icon:'none'});}catch(_){wx.showToast({title:'保存失败，请检查存储空间',icon:'none'});}},
 map(){wx.showToast({title:'导航模块由成员5接入并核验坐标',icon:'none'});},
 routes(){wx.switchTab({url:'/pages/routes/routes'});}
});

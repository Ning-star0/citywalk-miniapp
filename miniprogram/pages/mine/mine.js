const repo=require('../../services/catalog');const favorites=require('../../services/favorites');
Page({data:{routes:[]},onShow(){this.setData({routes:favorites.list().map(id=>repo.detail(id)).filter(Boolean)});},open(e){wx.navigateTo({url:'/pages/detail/detail?id='+e.currentTarget.dataset.id});}});

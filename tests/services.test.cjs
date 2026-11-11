const {test}=require('node:test');
const assert=require('node:assert/strict');
const repo=require('../miniprogram/services/catalog');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const {createRequire}=require('node:module');

test('默认不推荐草案，开发模式显式可见',()=>{
 assert.equal(repo.list().length,0);
 assert.equal(repo.list({includeDrafts:true}).length,2);
});
test('组合搜索和总耗时边界',()=>{
 assert.equal(repo.list({includeDrafts:true,keyword:'甲秀楼',district:'待核验商圈A',maxMinutes:85}).length,1);
 assert.equal(repo.list({includeDrafts:true,keyword:'甲秀楼',district:'待核验商圈A',maxMinutes:84}).length,0);
 assert.equal(repo.list({includeDrafts:true,metroStation:'未知站'}).length,0);
});
test('详情展开引用和非法ID',()=>{
 assert.equal(repo.detail('bad'),null);
 const r=repo.detail('gyr_001');
 assert.equal(r.stops[0].point.id,'gyp_001');
 assert.equal(r.totalMinutes,r.walkingMinutes+r.stayingMinutes);
});
test('收藏写入失败不会返回成功',()=>{
 const values=new Map();
 global.wx={getStorageSync:k=>values.get(k)||'',setStorageSync:(k,v)=>values.set(k,v)};
 const store=require('../miniprogram/services/favorites');
 assert.equal(store.toggle('gyr_001'),true);
 assert.deepEqual(store.list(),['gyr_001']);
 assert.equal(store.toggle('gyr_001'),false);
 values.set('citywalk:favorites:v1','corrupt');
 assert.deepEqual(store.list(),[]);
 wx.setStorageSync=()=>{throw Error('quota');};
 assert.throws(()=>store.toggle('gyr_001'),/quota/);
});
test('已注册页面存在，WXML事件均有处理函数',()=>{
 const base=path.join(__dirname,'../miniprogram');
 const app=JSON.parse(fs.readFileSync(path.join(base,'app.json'),'utf8'));
 app.pages.forEach(relative=>{
  const file=path.join(base,relative+'.js');
  assert.ok(fs.existsSync(file));
  JSON.parse(fs.readFileSync(path.join(base,relative+'.json'),'utf8'));
  let definition;
  vm.runInNewContext(fs.readFileSync(file,'utf8'),{Page:value=>{definition=value;},require:createRequire(file),wx:{}},{filename:file});
  const wxml=fs.readFileSync(path.join(base,relative+'.wxml'),'utf8');
  for(const match of wxml.matchAll(/(?:bind|catch)(?::)?[a-z]+="([^"]+)"/g)){
   assert.equal(typeof definition[match[1]],'function',relative+' 缺少事件 '+match[1]);
  }
 });
});

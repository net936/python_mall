<template>
  <div class="content-list">
    <div class="list-title">我的订单</div>
    <a-spin :spinning="loading" style="min-height: 200px">
      <div class="list-content">
        <div class="order-item-view" v-for="(item, index) in orderData" :key="index">
          <div class="header flex-view">
            <div class="left">
              <span class="text">订单号</span>
              <span class="num mg-4">#</span>
              <span class="num">{{ item.order_number }}</span>
              <span class="time">{{ item.order_time }}</span>
            </div>
            <div class="right">
              <a-popconfirm v-if="item.status === '1'" title="确定取消订单？" ok-text="是" cancel-text="否" @confirm="handleCancel(item)">
                <a-button type="primary" size="small" style="margin-right: 24px">取消</a-button>
              </a-popconfirm>
              <span class="text">状态</span>
              <span class="state">{{ item.status === '1' ? '正常' : '已取消' }}</span>
            </div>
          </div>
          <div class="content flex-view">
            <div class="left-list">
              <div class="list-item flex-view" v-for="gwcItem in item.gwcData">
                <div class="detail">
                  <div class=" flex-top flex-view">
                    <h2 class="name">{{gwcItem.title}}</h2>
                    <span class="count" style="margin-left: 4px;">x{{gwcItem.count}}</span>
                  </div>
                  <div class="flex-between flex-view" style="margin-left: auto;">
                    <span class="type"></span>
                    <span class="price">¥{{gwcItem.price}}</span>
                  </div>
                </div>
              </div>
            </div>

          </div>
          <div class="bottom flex-view">
            <div class="left">
              <span class="text"></span>
            </div>
            <div class="right flex-view">
              <span class="text">总计</span>
              <span class="num">¥ {{item.amount}}</span>
              <span class="text">优惠</span>
              <span class="num">¥0</span>
              <span class="text">共支付</span>
              <span class="money">¥ {{item.amount}}</span>
            </div>
          </div>
        </div>
        <template v-if="!orderData || orderData.length <= 0">
          <a-empty style="width: 100%; margin-top: 200px" />
        </template>
      </div>
    </a-spin>
  </div>
</template>

<script setup>
  import { message } from 'ant-design-vue';
  import { userOrderListApi } from '/@/api/index/order';
  import { cancelUserOrderApi } from '/@/api/index/order';
  import { BASE_URL } from '/@/store/constants';
  import { useUserStore } from '/@/store';

  const router = useRouter();
  const route = useRoute();
  const userStore = useUserStore();

  const loading = ref(false);
  const orderData = ref([]);
  const orderStatus = ref('');

  onMounted(() => {
    getOrderList();
  });

  const onTabChange = (key) => {
    console.log(key);
    if (key === '1') {
      orderStatus.value = '';
    }
    if (key === '2') {
      orderStatus.value = '1';
    }
    if (key === '3') {
      orderStatus.value = '2';
    }
    getOrderList();
  };
  const getOrderList = () => {
    loading.value = true;
    let userId = userStore.user_id;
    userOrderListApi({ userId: userId, orderStatus: orderStatus.value })
      .then((res) => {
        res.data.forEach((item, index) => {
          if (item.cover) {
            item.cover = BASE_URL + item.cover;
          }
          if(item.gwc) {
            let obj = JSON.parse(item.gwc);
            item.gwcData = obj['gwc']
          }
        });
        orderData.value = res.data;
        loading.value = false;
      })
      .catch((err) => {
        console.log(err);
        loading.value = false;
      });
  };
  const handleDetail = (thingId) => {
    // 跳转新页面
    let text = router.resolve({ name: 'detail', query: { id: thingId } });
    window.open(text.href, '_blank');
  };
  const handleCancel = (item) => {
    cancelUserOrderApi({
      id: item.id,
    })
      .then((res) => {
        message.success('取消成功');
        getOrderList();
      })
      .catch((err) => {
        message.error(err.msg || '取消失败');
      });
  };
</script>
<style scoped lang="less">
  .flex-view {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
  }

  .content-list {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;

    .list-title {
      color: #152844;
      font-weight: 600;
      font-size: 18px;
      line-height: 24px;
      height: 24px;
      margin-bottom: 4px;
    }
  }

  .order-item-view {
    background: #f7f9fb;
    border-radius: 4px;
    padding: 16px;
    margin-top: 12px;

    .header {
      border-bottom: 1px solid #cedce4;
      padding-bottom: 12px;
      -webkit-box-pack: justify;
      -ms-flex-pack: justify;
      justify-content: space-between;
      font-size: 14px;

      .text {
        color: #6f6f6f;
      }

      .mg-4 {
        margin-left: 4px;
      }

      .num {
        font-weight: 500;
        color: #152844;
      }

      .num {
        font-weight: 500;
        color: #152844;
      }

      .time {
        margin-left: 16px;
        color: #a1adc5;
      }

      .state {
        color: #ff7b31;
        font-weight: 600;
        margin-left: 10px;
      }
    }

    .content {
      padding: 12px 0;
      overflow: hidden;

      .left-list {
        overflow: hidden;
        min-height: 40px;
        -webkit-box-flex: 2;
        -ms-flex: 2;
        flex: 2;
        padding-right: 16px;

        .list-item {
          height: 30px;
          margin-bottom: 12px;
          overflow: hidden;
        }

        .thing-img {
          width: 60px;
          height: 60px;
          margin-right: 12px;
          object-fit: cover;
        }

        .detail {
          -webkit-box-flex: 1;
          -ms-flex: 1;
          flex: 1;
          display: flex;
          -ms-flex-direction: row;
          flex-direction: row;
        }

        .flex-between {
          -webkit-box-pack: justify;
          -ms-flex-pack: justify;
          justify-content: space-between;
        }

        .flex-between {
          -webkit-box-pack: justify;
          -ms-flex-pack: justify;
          justify-content: space-between;
        }

        .flex-top {
          -webkit-box-align: start;
          -ms-flex-align: start;
          align-items: flex-start;
        }

        .name {
          color: #152844;
          font-weight: 400;
          font-size: 15px;
          line-height: 18px;
        }

        .count {
          color: #484848;
          font-size: 12px;
        }

        .flex-between {
          -webkit-box-pack: justify;
          -ms-flex-pack: justify;
          justify-content: space-between;
        }

        .flex-center {
          -webkit-box-align: center;
          -ms-flex-align: center;
          align-items: center;
        }

        .type {
          color: #6f6f6f;
          font-size: 12px;
        }

        .price {
          color: #ff7b31;
          font-weight: 600;
          font-size: 14px;
        }
      }

      .right-info {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
        border-left: 1px solid #cedce4;
        padding-left: 12px;
        line-height: 22px;
        font-size: 14px;

        .title {
          color: #6f6f6f;
        }

        .name {
          color: #152844;
        }

        .text {
          color: #484848;
        }

        .mg {
          margin-bottom: 4px;
        }
      }
    }

    .bottom {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
      border-top: 1px solid #cedce4;
      -webkit-box-pack: justify;
      -ms-flex-pack: justify;
      justify-content: space-between;
      font-size: 14px;
      padding-top: 14px;

      .text {
        color: #6f6f6f;
      }

      .open {
        color: #4684e2;
        margin-left: 8px;
        cursor: pointer;
      }

      .right {
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
      }

      .text {
        color: #6f6f6f;
      }

      .num {
        color: #152844;
        margin: 0 40px 0 8px;
      }

      .money {
        font-weight: 600;
        font-size: 18px;
        color: #ff7b31;
        margin-left: 8px;
      }
    }
  }

  .order-item-view:first-child {
    margin-top: 16px;
  }
</style>

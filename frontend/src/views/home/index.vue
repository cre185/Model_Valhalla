<template>
  <section class="home">
    <div class="home-content">
      <h3>{{ $t('home.hello') }}</h3>
      <h1>{{ $t('home.this') }}模型竞技场 Model Valhalla</h1>
      <h3>{{ $t('home.face') }}<span id="multiple-text"></span></h3>
      <p> {{ $t('home.target') }} </p>
      <a class="btn" @click="Login">Get Started</a>
    </div>
    <a-space direction="vertical" :size="40" style="display: block">
      <a-row class="grid-demo">
        <a-col :span="11">
          <a-card
            id="card1"
            class="card"
            :body-style="{
              color: '#1f242d',
            }"
            :bordered="false"
          >
            {{ $t('home.dataset') }}
          </a-card>
        </a-col>
        <a-col :span="2"></a-col>
        <a-col :span="11">
          <a-card
            id="card2"
            class="card"
            :body-style="{
              color: '#1f242d',
            }"
            :bordered="false"
          >
            {{ $t('home.ranking') }}
          </a-card>
        </a-col>
      </a-row>
      <a-row class="grid-demo">
        <a-col :span="11">
          <a-card
            id="card3"
            class="card"
            :body-style="{
              color: '#1f242d',
            }"
            :bordered="false"
          >
            {{ $t('home.info') }}
          </a-card>
        </a-col>
        <a-col :span="2"></a-col>
        <a-col :span="11">
          <a-card
            id="card4"
            class="card"
            :body-style="{
              color: '#1f242d',
            }"
            :bordered="false"
          >
            {{ $t('home.rule') }}
          </a-card>
        </a-col>
      </a-row>
      <a-row class="grid-demo">
        <a-col :span="11">
          <a-card
            id="card5"
            class="card"
            :body-style="{
              color: '#1f242d',
            }"
            :bordered="false"
          >
            {{ $t('home.discussion') }}
          </a-card>
        </a-col>
        <a-col :span="2"></a-col>
        <a-col :span="11">
          <a-card
            id="card6"
            class="card"
            :body-style="{
              color: '#1f242d',
            }"
            :bordered="false"
          >
            {{ $t('home.user') }}
          </a-card>
        </a-col>
      </a-row>
    </a-space>
  </section>
</template>

<script>
  import Typed from 'typed.js';
  import { useRouter } from 'vue-router';
  import { isLogin } from "@/utils/auth";
  import { useI18n } from "vue-i18n";
  import {onBeforeUpdate, onMounted, ref} from "vue";
  import useLocale from "@/hooks/locale";

  export default {
    setup() {
      const { t } = useI18n();
      const typedRef = ref();
      const router = useRouter();
      const { currentLocale } = useLocale();
      const Login = () => {
        if (isLogin()) {
          router.push({
            name: 'leaderboardDetails',
          });
        }
        else {
          router.push({
            name: 'Login',
          });
        }
      };
      onBeforeUpdate(() => {
        typedRef.value.destroy();
        typedRef.value = new Typed('#multiple-text', {
          strings: [`${t('home.people1')}`, `${t('home.people2')}`, `${t('home.people3')}`, `${t('home.people4')}`],
          typeSpeed: 100,
          backSpeed: 100,
          backDelay: 1000,
          loop: true,
        });
      });
      onMounted(() => {
        typedRef.value = new Typed('#multiple-text', {
          strings: [`${t('home.people1')}`, `${t('home.people2')}`, `${t('home.people3')}`, `${t('home.people4')}`],
          typeSpeed: 100,
          backSpeed: 100,
          backDelay: 1000,
          loop: true,
        });
      });
      return { Login };
    },
  };
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Poppins', sans-serif;
  }

  .home {
    position: relative;
    background: white;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 70px 5% 0 5%;
  }

  .home-content {
    max-width: 600px;
    transform: translateY(-3%);
  }

  .home-content h3 {
    font-size: 40px;
    font-weight: 700;
    line-height: 2em;
    opacity: 0;
    animation: slideBottom 1s ease forwards;
    animation-delay: 0.7s;
  }

  .home-content h3:nth-of-type(2) {
    margin-bottom: 30px;
    opacity: 0;
    animation: slideTop 1s ease forwards;
    animation-delay: 0.7s;
  }

  .home-content h3 span {
    color: #1c61ff;
  }

  .home-content h1 {
    font-size: 70px;
    font-weight: 700;
    margin: -3px 0;
    opacity: 0;
    animation: slideRight 1s ease forwards;
    animation-delay: 1s;
  }

  .home-content p {
    font-size: 20px;
    opacity: 0;
    animation: slideLeft 1s ease forwards;
    animation-delay: 0.7s;
  }

  .home-img img {
    max-width: 450px;
    border-radius: 50%;
    margin-right: -20px;
    box-shadow: 0 0 20px #b7b2a9;
    opacity: 0;
    animation: zoomIn 1s ease forwards, floatImage 4s ease-in-out infinite;
    animation-delay: 2s, 3s;
  }

  .btn {
    display: inline-block;
    margin-top: 7%;
    padding: 18px 50px;
    background: #1c61ff;
    text-decoration: none;
    border-radius: 40px;
    box-shadow: 0 0 10px royalblue;
    font-size: 16px;
    color: white;
    letter-spacing: 1px;
    font-weight: 600;
    transition: 0.5s ease;
    opacity: 0;
    animation: slideTop 1s ease forwards;
    animation-delay: 2s;
  }

  .btn:hover {
    background: white;
    color: black;
    box-shadow: 0 0 10px #1c61ff;
  }

  @keyframes slideRight {
    0% {
      transform: translateX(-100px);
    }

    100% {
      transform: translateX(0);
      opacity: 1;
    }
  }

  @keyframes slideLeft {
    0% {
      transform: translateX(100px);
    }

    100% {
      transform: translateX(0);
      opacity: 1;
    }
  }

  @keyframes slideTop {
    0% {
      transform: translateY(100px);
    }

    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }

  @keyframes slideBottom {
    0% {
      transform: translateY(-100px);
    }

    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }

  @keyframes zoomIn {
    0% {
      transform: scale(0);
    }

    100% {
      transform: scale(1);
      opacity: 1;
    }
  }

  @keyframes zoomInMove {
    0% {
      transform: translateX(-20%) scale(0);
    }

    100% {
      transform: translateX(-20%) scale(1);
      opacity: 1;
    }
  }

  @keyframes floatImage {
    0% {
      transform: translateY(0);
    }

    50% {
      transform: translateY(-24px);
    }

    100% {
      transform: translateY(0);
    }
  }

  @keyframes floatImageMove {
    0% {
      transform: translate(-20%, 0);
    }

    50% {
      transform: translate(-20%, -24px);
    }

    100% {
      transform: translate(-20%, 0);
    }
  }

  .card {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 30px 30px 30px 30px;
    width: 250px;
    height: 150px;
    font-family: DouYin;
    font-size: 16px;
    font-weight: 700;
  }

  #card1 {
    background: url('../../assets/images/index_1.jpg');
    background-size: 250px 200px;
    box-shadow: 0 0 20px #b7b2a9;
    opacity: 0;
    animation: zoomIn 1s ease forwards, floatImage 4s ease-in-out infinite;
    animation-delay: 2s, 3s;
  }

  #card2 {
    background: url('../../assets/images/index_2.jpg');
    background-size: 250px 200px;
    box-shadow: 0 0 20px #b7b2a9;
    opacity: 0;
    animation: zoomIn 1s ease forwards, floatImage 4s ease-in-out infinite;
    animation-delay: 2s, 3s;
  }

  #card3 {
    background: url('../../assets/images/index_3.jpg');
    background-size: 250px 200px;
    box-shadow: 0 0 20px #b7b2a9;
    opacity: 0;
    animation: zoomInMove 1s ease forwards,
      floatImageMove 4s ease-in-out infinite;
    animation-delay: 2s, 3s;
  }

  #card4 {
    background: url('../../assets/images/index_4.jpg');
    background-size: 250px 200px;
    box-shadow: 0 0 20px #b7b2a9;
    opacity: 0;
    animation: zoomInMove 1s ease forwards,
      floatImageMove 4s ease-in-out infinite;
    animation-delay: 2s, 3s;
  }

  #card5 {
    background: url('../../assets/images/index_5.jpg');
    background-size: 250px 200px;
    box-shadow: 0 0 20px #b7b2a9;
    opacity: 0;
    animation: zoomIn 1s ease forwards, floatImage 4s ease-in-out infinite;
    animation-delay: 2s, 3s;
  }

  #card6 {
    background: url('../../assets/images/index_6.jpg');
    background-size: 250px 200px;
    box-shadow: 0 0 20px #b7b2a9;
    opacity: 0;
    animation: zoomIn 1s ease forwards, floatImage 4s ease-in-out infinite;
    animation-delay: 2s, 3s;
  }
</style>

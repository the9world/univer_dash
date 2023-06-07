import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # st.title("University Ranking in the UK")University Ranking in the UK
    st.markdown("""<span style='color:red; font-size:50px; font-weight:bold;'>University Ranking </span>
                <span style='color:black; font-size:20px;'> in the</span>
                <span style='color:blue; font-size:50px; font-weight:bold;'>UK</span>""",
                unsafe_allow_html=True)
    new_title = '<p style="font-family:sans-serif; color:purple; font-size: 50px;">University Ranking in the UK</p> '
    st.markdown(new_title, unsafe_allow_html=True)
    menu= ['Home', 'EDA', 'ML']
    choice = st.sidebar.selectbox('메뉴', menu)
    
    if choice == menu[0] :
        # run_app_home()
            st.markdown("This text is :red[colored red], and this is **:blue[colored]** and bold.")
            st.markdown("""<span style='color:red; font-size:24px; font-weight:bold;'>This</span>
                           <span style='color:blue; font-size:24px; font-weight:bold;'>larger</span>""",
                           unsafe_allow_html=True)

            st.text('좋은 서비스를 제공하겠습니다.')
            st.text('자동 배포 처리된 앱입니다.')
            img_url= 'https://www.irishtimes.com/resizer/pPJML7tkKkfBuXUYNfRzjnQxqjI=/1600x0/filters:format(jpg):quality(70)/cloudfront-eu-central-1.images.arcpublishing.com/irishtimes/XPHTWNJW3THZZ3UTNI3RDXXOPE.jpg'

            st.image(img_url)
    
    elif choice == menu[1] :
        # run_app_eda()

        st.subheader('데이터 분석')
        
        df= pd.read_csv(r"C:\Users\5\Documents\GitHub\univer_dash\data\university_UK.csv")
        print(df)
        
        if st.checkbox('데이터 프레임 보기') :
            st.dataframe(df)

        st.subheader('기본 통계 데이터')
        st.dataframe(df.describe())
        
        st.subheader('최대 / 최소 데이터 확인하기')
        # st.selectbox('컬럼을 선택하세요', df.columns) # 문자열 컬럼 제외 해야함
        column = st.selectbox('컬럼을 선택하세요', df.columns[ 4 : ] )

        st.success('최대 데이터') # 유저가 선택한 컬럼의 최소, 최대 값을 보여줌
        st.dataframe( df.loc[df[column]== df[column].max(), ] )    
        st.success('최소 데이터')
        st.dataframe( df.loc[df[column]== df[column].min(), ] )
        
        st.subheader('컬럼 별 히스토그램') 
        # column = st.selectbox('컬럼을 선택하세요', df.columns[ 3 : ] ) # 이대로는 line 20과 동일하여 error 발생
        column = st.selectbox('히스토그램 확인할 컬럼을 선택하세요', df.columns[ 3 : ] ) # 숫자 데이터만 보기
        bins = st.number_input('빈의 갯수를 입력하세요. 10 ~ 30', 10, 30, 20) # bins의 갯수를 유저에게 받음
        
        fig= plt.figure() # 영역 잡아주기
        df[column].hist(bins=bins) # df[유저가 선택한 컬럼(변수) 입력]
        plt.title(column + " Histogram") # 그래프 타이틀
        plt.xlabel(column) # x축 이름
        plt.ylabel("count") # y축 이름
        st.pyplot(fig)
        
        # 유저에게 컬럼 선택권을 줌 (상관계수, corr)
        st.subheader('상관 관계 분석')
        column_list= st.multiselect('상관분석 하고싶은 컬럼을 선택하세요', df.columns[ 3 : ] ) # 숫자 데이터만 보기
        # 여러개 하려면 list로 해야함 : data=df[column_list].corr() 상관계수
        
        # 2개 이상 선택하면 히스토그램 출력하기
        if len(column_list) >= 2:
            fig2 = plt.figure()
            sns.heatmap(data=df[column_list].corr(), annot=True, vmin=-1, vmax=1,
                    cmap='coolwarm', fmt='.2f', linewidths= 0.5)
            st.pyplot(fig2)    
        else:
            st.error('2개 이상 선택하세요')
    
    else :
        # run_app_ml()
        st.subheader('자동차 금액 예측')
        
        # 성별, 나이, 연봉, 카드빚, 자산을 유저한테 입력 받는다.
        gender= st.radio('성별 선택', ['남자', '여자'])
        if gender =='남자' :
            gender = 0 # 유저 입력 값을 이진수로 변환
        else :
            gender = 1
        
        age = st.number_input('나이 입력', 18, 100) # 유저에게 입력 받을 나이(숫자)
        salary = st.number_input('연봉 입력', 5000, 1000000) # 파라미터 최소, 최대범위
        debt = st.number_input('카드 빚', 0, 1000000)
        worth = st.number_input('자산 입력', 1000, 10000000)
        
        # 턴을 누르면 예측한 금액을 표시한다.
        if st.button('금액 예측'): 
            new_data = np.array( [ gender, age, salary, debt, worth ] ) # 여러개면 꼭 []
            new_data = new_data.reshape(1, 5) # 입력 받은 값을 2차원으로 변환 : 1행 5열
        
            # regressor 불러오기, 학습한 데이터 가져오기
            regressor = joblib.load('model/regressor.pkl')
            y_pred = regressor.predict(new_data)
            print(y_pred)
                    
            # 28220달러 짜리 차량 구매 가능합니다. 출력
            print(y_pred[0]) # 왜 y_pred[0]이 숫자?
            print( round( y_pred[0] ) ) # 반올림
            price = ( round( y_pred[0] ) )
            
            # st.text(str(price) + '달러짜리 차량 구매 가능합니다.')
            # st.text('{}달러 짜리 차량 구매 가능합니다.').format(y_pred)
            # st.text(f'{y_pred[0]: .1f}달러짜리 차량 구매 가능합니다.')
            st.text(f"{int(y_pred[0])}달러 짜리 차량 구매 가능합니다.")
            print((f"{int(y_pred[0])}달러 짜리 차량 구매 가능합니다."))
    
    
if __name__=='__main__':
    main()
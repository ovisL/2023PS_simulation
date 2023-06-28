import simpy

def car(env) :
    def __init__(self,env) :
        self.env = env
        self.proc = env.process(self.run()) # run을 프로세스에 등록
        
    def charge(self,duration) :
        yield self.env.timeout(duration)
            
    def run(self) :
        while True:
            print('Start parking and charging at %d' % env.now) 
            # parking_duration = 5
            charge_duration = 5
            yield env.process(self.charge(charge_duration))
            # yield env.timeout(parking_duration) 
            # 함수를 끝내지 않은 상태에서 yield를 사용하여 값을 바깥으로 전달 가능
            # 즉 return과 다르게 잠시 함수 바깥의 코드가 실행되도록 양보하여 값을 가져가게 한뒤 다시 제너레이터 안의 코드를 계속 실행
            print('Start driving at %d' % env.now) 
            trip_duration = 2
            yield env.timeout(trip_duration)
 
env = simpy.Environment() # 환경 정의
# env.process(car(env))  # env에 car 프로세스 등록
car = car(env)
env.run(until=30) # 시간 30이 될때까지 실행

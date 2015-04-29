
DEBUG = __name__ == '__main__' and False #or True

class GasStations(object):
    '''
    This class is to solve the problem:
Using the Python language, have the function GasStation(strArr) 
take strArr which will be an an array consisting of the following 
elements: N which will be the number of gas stations in a circular 
route and each subsequent element will be the string g:c where g is 
the amount of gas in gallons at that gas station and c will be the 
amount of gallons of gas needed to get to the following gas station. 
For example strArr may be: ["4","3:1","2:2","1:2","0:1"]. 
Your goal is to return the index of the starting gas station that will 
allow you to travel around the whole route once, otherwise return the 
string impossible. For the example above, there are 4 gas stations, 
and your program should return the string 1 because starting at station 
1 you receive 3 gallons of gas and spend 1 getting to the next station. 
Then you have 2 gallons + 2 more at the next station and you spend 2 so 
you have 2 gallons when you get to the 3rd station. 
You then have 3 but you spend 2 getting to the final station, and at the 
final station you receive 0 gallons and you spend your final gallon getting 
to your starting point. Starting at any other gas station would make getting 
around the route impossible, so the answer is 1. 
If there are multiple gas stations that are possible to start at, 
return the smallest index (of the gas station). 
N will be >= 2. 

    Example for Python: 
>>> import gas
>>> g = gas.GasStations(["4","3:1","2:2","1:1","0:0"])
>>> print g.result()

    Example for WEB:
    Put the string array like this: 4,3:1,2:2,1:1,0:0 and click the button.
    '''
    _gasStations = []
    
    # Constants
    SEP = ':'
    
    # Messages
    MSG_INVALID_GAS_STATIONS = 'is not a valid string array of gas stations!'
    MSG_IMPOSSIBLE = 'impossible'
    
    def __init__(self, gasStations=None):
        '''
        gasStations must be a string array that your first element is a 
integer "N", where "N" is the number of stations on the route.
        '''
        self.gasStations = gasStations
    
    def is_valid_gasStations(self, gasStations=None):
        '''
        This method just verify if the gasStations variable is a valid string
array of stations route.
        '''
        if gasStations is None:
            gasStations = self.gasStations
        if type(gasStations) != type(self._gasStations):
            if DEBUG: print 'invalid case 1';
            return False
        if len(gasStations) < 2:
            if DEBUG: print 'invalid case 2';
            return False
        try:
            if int(gasStations[0]) != len(gasStations)-1:
                if DEBUG: print 'invalid case 3';
                return False
        except:
            if DEBUG: print 'invalid case 4';
            return False
        for i in gasStations[1:]:
            if type(i) != type(''):
                if DEBUG: print 'invalid case 5';
                return False
            if self.SEP in i:
                g,c = i.split(self.SEP)
                if not g.isdigit() or not c.isdigit():
                    if DEBUG: print 'invalid case 6';
                    return False
            else:
                return False
        return True
    
    def _set_gasStations(self, value):
        if self.is_valid_gasStations( value ):
            # Just set a valid string array of stations route
            self._gasStations = value
        else:
            print value, self.MSG_INVALID_GAS_STATIONS
    def _get_gasStations(self,):
        return self._gasStations
    gasStations = property(_get_gasStations, _set_gasStations)
    
    def get_g_and_c(self, n):
        '''
        This method get the g (amount of gas in gallons at that gas station) 
and c (amount of gallons of gas needed to get to the following gas station) at
the position "n" of string array of stations route.
        '''
        try:
            n = int(n)
            i = self.gasStations[n]
            if self.SEP in i:
                g,c = i.split(self.SEP)
            else:
                g,c = i, None
        except:
            g,c = None, None
        return int(g), int(c)
    
    def get_last_station(self, n=None):
        '''
        This method follow the circular route that start at "n" position.
        
        Inputs:
            "n": the start position to verify if this route is possible.
            
        Return:
            a tuple with two elements like that (s, n), where:
                "s" is the amount of gallons that would be left after moving 
                    to the next station;
                "n" is the position of the station could be achieved
        
        Note:
            If s<0 this means there is not enough gallons to get to the next 
            station.
            If input "n" is equal output "n", then this route is possible!
        '''
        try:
            if n is None:
                n = 1       # Initial position of string array
            i = n = int(n)      # Only integer is a valid position!
            s = 0           # Initial gallons
            while n > 0:
                g,c = self.get_g_and_c(n)
                s += g - c  # Calcule the amount of gallons
                if DEBUG: print 'n =', n, 'g =', g, 'c =', c, 's =', s;
                n += 1      # Set to next position
                if s < 0:
                    break   # This route is not possible!
                if n == len(self.gasStations):
                    n = 1   # Set initial position because is a circular route!
                if i == n:
                    break   # This route is possible!
            return s, n # Return "s" (gallons resultants) and actual position
        except:
            return -1, n
    
    def result(self,):
        if self.is_valid_gasStations():
            for i in xrange(len(self.gasStations)):
                if i == 0: continue;
                s,n = self.get_last_station(i)
                if i == n:  # The route started at "i" is possible
                    return str(n)
            return self.MSG_IMPOSSIBLE
        msg = self.MSG_INVALID_GAS_STATIONS
        return msg

if __name__ == '__main__':
    samples = [
        ['4',"3:1","2:2","1:1","0:0"],
        ["4","3:1","2:2","1:2","0:1"],
        ["4","1:1","2:2","1:2","0:1"],
        ["4","0:1","2:2","1:2","3:1"],
        ["4","0:1","4:3","1:2","3:1"],
    ]
    for sample in samples:
        g = GasStations(sample)
        print 'Testing for', g.gasStations
        print g.result()

    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator
    from pyramid.response import Response
    
    def main(request):
        data = request.POST.get('data')
        if data:    # Is a POST method
            d = { 'data': data, 'info': '', 'result': '' }
            data = str(data).split(',')
            g = GasStations( data )
            d.update({'result': 'Result: %s' %g.result()})
        else:
            g = GasStations()
            d = { 'data': '', 'info': '', 'result': '' }
        info = g.__doc__.replace('\n    ', '</p><p class="info">')\
            .replace('\n>>>', '<br />>>>')#.replace('\n1', '<br />1')
        d.update({'info': '<p class="info">%s</p>' %info})
        f = open('gas.html')
        msg = f.read()
        msg = msg %d
        return Response(msg)
        return Response('Teste: <ul><li>%(action)s;</li><li>%(data)s.</li></ul>' % request.matchdict)
    
    config = Configurator()
    config.add_route('main', '/main' )
    config.add_view(main, route_name='main')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()


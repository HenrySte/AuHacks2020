# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils
import random

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

categories = "animals and blocks in minecraft."
blockArray = ["stone", "granite", "grass", "dirt", "cobblestone", "oak wood plank", "spruce wood plank", "birch wood plank", "jungle wood plank", "acacia wood plank", "dark oak wood plank", "bedrock", "sand", "gravel", "gold ore", "iron ore", "coal ore", "oak wood", "spruce wood", "birch wood", "jungle wood", "oak leaves", "spruce leaves", "birch leaves", "jungle leaves", "sponge", "glass", "lapis ore", "lapis block", "sand stone", "note block", "piston", "sticky piston", "wool", "dispenser", "gold block", "iron block", "brick", "tee in tee", "bookshelf", "moss stone", "obsidian", "chest", "diamond block", "diamond ore", "crafting table", "furnace", "red stone ore", "snow", "ice", "cactus", "clay", "jukebox", "pumpkin", "nether rack", "soul sand", "glow stone", "stained glass", "stone bricks", "mushroom block", "melon block", "mycelium", "nether brick", "end stone", "red stone lamp", "emerald ore", "emerald block", "beacon", "red stone block", "quartz", "dropper", "hardened clay", "acacia leaves", "dark oak leaves", "acacia wood", "dark oak wood", "slime block", "sea lantern", "hay bale", "block of coal", "packed ice", "magma block", "bone block", "observer"]
fruitArray = ["apple", "apricot", "avocado", "banana", "blackberry", "blueberry", "cantaloupe", "cherry", "clementine", "coconut", "cranberry", "date", "durian", "fig", "grapefruit", "grape", "guava", "honeydew melon", "plum", "kiwi", "lemon", "lime", "mandarin", "mango", "nectarine", "olive", "orange", "papaya", "passion fruit", "peach", "pear", "dragonfruit", "pineapple", "plantain", "plum", "pomegranate", "raspberry", "strawberry", "tangerine", "watermelon"]
remainingValues = []
roundCount = 1
eventName = "start"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, to the categories game! Do you know how to play?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class NoContinueIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        if (ask_utils.is_intent_name("NoIntent")(handler_input) and eventName == "lose") :
            return ask_utils.is_intent_name("NoIntent")(handler_input)
    
    def handle(self, handler_input):
        speak_output = "Thanks for playing. Goodbye."
        return (
            handler_input.response_builder
                .speak(speak_output)
                #.ask("test test")
                .response
        )

class YesPlayIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        if (ask_utils.is_intent_name("YesIntent")(handler_input) and (eventName == "start" or eventName == "lose")) :
            return ask_utils.is_intent_name("YesIntent")(handler_input)
    
    def handle(self, handler_input): 
        global eventName
        global remainingValues
        global roundCount
        if (eventName == "lose") :
            reset()
        speak_output = "Pick a category. The categories are " + categories + " Say fruit or block."
        eventName = "quiz"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("test test")
                .response
        )

class NoPlayIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        if (ask_utils.is_intent_name("NoIntent")(handler_input) and eventName == "start") :
            return ask_utils.is_intent_name("NoIntent")(handler_input)
    
    def handle(self, handler_input):
        speak_output = "First, pick a category from the list provided. You and I take turns saying words from that category. The first to not come up with a valid answer loses. I’ll keep score, and let you know how you did at the end. See how long you can last! Say yes to continue."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("test test")
                .response
        )


class PickCategoryIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        if (ask_utils.is_intent_name("CategoriesIntent")(handler_input) and eventName == "quiz") :
            return ask_utils.is_intent_name("CategoriesIntent")(handler_input)
    
    def handle(self, handler_input):
        slots  = handler_input.request_envelope.request.intent.slots
        pick = slots['categorySlot'].value
        global remainingValues
        global roundCount
        global eventName
        if (pick == "block"):
            remainingValues = blockArray.copy()
            eventName = "block"
        elif (pick == "fruit"):
            remainingValues = fruitArray.copy()
            eventName = "fruit"
        alexasChoice = alexaTurn()
        speak_output = "You picked " + pick + ". Round " + str(roundCount) + ". I will go first. I pick " + alexasChoice + ". Your turn!"
        roundCount += 1
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class BlockIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        if (ask_utils.is_intent_name("BlockIntent")(handler_input) and eventName == "block") :
            return ask_utils.is_intent_name("BlockIntent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots  = handler_input.request_envelope.request.intent.slots
        userAnswer = slots['blockSlot'].value
        global remainingValues
        global roundCount
        global eventName
        if(userAnswer in remainingValues):
            alexasChoice = alexaTurn()
            speak_output = "You picked " + userAnswer + ". Round " + str(roundCount) + ". My turn, I pick " + alexasChoice + "."
            remainingValues.remove(userAnswer)
            roundCount += 1
        else:
            speak_output = "You repeated a word! You lose, you survived " + str(roundCount - 2) + " rounds. Do you want to try again?"
            eventName = "lose"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class FruitIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        if (ask_utils.is_intent_name("FruitIntent")(handler_input) and eventName == "fruit") :
            return ask_utils.is_intent_name("FruitIntent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots  = handler_input.request_envelope.request.intent.slots
        userAnswer = slots['fruitSlot'].value
        global remainingValues
        global roundCount
        global eventName
        if(userAnswer in remainingValues):
            alexasChoice = alexaTurn()
            speak_output = "You picked " + userAnswer + ". Round " + str(roundCount) + ". My turn, I pick " + alexasChoice + "."
            remainingValues.remove(userAnswer)
            roundCount += 1
        else:
            speak_output = "You repeated a word! You lose, you survived " + str(roundCount - 2) + " rounds. Do you want to try again?"
            eventName = "lose"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "First pick a category, to do rest. The categories are fruit, and Blocks of minecraft."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        #speak_output = "You just triggered " + intent_name + "."
        speak_output = "Invalid input, try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


def alexaTurn():
    global remainingValues
    random.seed()
    alexasChoice = random.choice(remainingValues)
    remainingValues.remove(alexasChoice)
    return (alexasChoice)

def reset():
    global remainingValues
    global roundCount
    global eventName
    remainingValues.clear()
    roundCount = 1
    eventName = "quiz"
    
'''
resolved_value = get_resolved_value(
            handler_input.request_envelope.request, "pet")
            '''




# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(PickCategoryIntentHandler())
sb.add_request_handler(BlockIntentHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(FruitIntentHandler())
sb.add_request_handler(NoContinueIntentHandler())
sb.add_request_handler(YesPlayIntentHandler())
sb.add_request_handler(NoPlayIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
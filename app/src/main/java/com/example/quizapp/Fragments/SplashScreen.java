package com.example.quizapp.Fragments;

import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import com.example.quizapp.MainActivity;
import com.example.quizapp.R;

import java.util.Timer;
import java.util.TimerTask;


public class SplashScreen extends Fragment {

    private MainActivity activity;


    public SplashScreen() {
        // Required empty public constructor
    }

    // TODO: Rename and change types and number of parameters
    public static SplashScreen newInstance() {
        Log.d("######", "Splashscreen#newInstance, 1");
        SplashScreen fragment = new SplashScreen();
        return fragment;
    }

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        Log.d("######", "Splashscreen#onAttach, 2");
        activity = (MainActivity) getActivity();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View v = inflater.inflate(R.layout.fragment_splash_screen, container, false);
        Timer timer = new Timer();
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
//                showing setup screen
                SetupScreen setupScreen = new SetupScreen();
                Log.d("######", "Splashscreen#run, 3");
//                activity.getSupportFragmentManager().popBackStack();
                activity.getSupportFragmentManager().beginTransaction().replace(R.id.main_activity, setupScreen).commit();
            }
        }, 1500);
        return v;
    }
}
